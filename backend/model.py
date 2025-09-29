import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV
import lightgbm as lgb
import joblib

# ---------------- Config ----------------
CONFIG = {
    'csv_paths': {
        'beneficiaries': 'beneficiary.csv',
        'repayment': 'repayment.csv',
        'aa': 'transactions.csv',
        'mobile': 'recharge.csv',
        'electric': 'electricity.csv',
        'pds': 'pds.csv',
        'other_utils': 'utilities.csv'
    },
    'model_dir': 'models/',
    'random_state': 42,
    'lgb_params': {
        'objective': 'binary',
        'metric': 'auc',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'seed': 42
    }
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_csv_safe(path):
    if not os.path.exists(path):
        print(f"Warning: CSV not found: {path}. Returning empty DataFrame")
        return pd.DataFrame()
    return pd.read_csv(path)

# ---------------- Feature Engineering ----------------
def build_features(config):
    cp = config['csv_paths']
    df_b = load_csv_safe(cp['beneficiaries'])
    df_repay = load_csv_safe(cp['repayment'])
    df_aa = load_csv_safe(cp['aa'])
    df_mob = load_csv_safe(cp['mobile'])
    df_elec = load_csv_safe(cp['electric'])

    if df_b.empty:
        raise ValueError("Beneficiaries CSV missing or empty.")

    # Basic features
    df_b['age'] = pd.to_datetime('today') - pd.to_datetime(df_b.get('date_of_birth', pd.NaT), errors='coerce')
    df_b['age'] = df_b['age'].dt.days / 365.25
    df_b['aadhaar_present'] = df_b.get('aadhaar_number', pd.NA).notna().astype(int)
    df_b['mobile_present'] = df_b.get('mobile_number', pd.NA).notna().astype(int)

    base = df_b.set_index('beneficiary_id')[['age','aadhaar_present','mobile_present','target_default']]

    # Repayment features
    if not df_repay.empty:
        df_repay['dpd_days'] = pd.to_numeric(df_repay.get('dpd_days',0), errors='coerce').fillna(0)
        repay_feats = df_repay.groupby('beneficiary_id').agg(
            num_emi_records=('emi_record_id','nunique'),
            total_emi_amount=('emi_amount','sum'),
            avg_dpd=('dpd_days','mean'),
            max_dpd=('dpd_days','max')
        ).fillna(0)
        base = base.join(repay_feats, how='left').fillna(0)

    # AA features
    if not df_aa.empty:
        df_aa['amount'] = pd.to_numeric(df_aa.get('amount',0), errors='coerce').fillna(0)
        df_aa['type'] = df_aa.get('type','').str.upper()
        credits = df_aa[df_aa['type']=='CREDIT'].groupby('beneficiary_id')['amount'].sum().rename('total_credit')
        debits = df_aa[df_aa['type']=='DEBIT'].groupby('beneficiary_id')['amount'].sum().rename('total_debit')
        aa_agg = pd.concat([credits,debits],axis=1).fillna(0)
        base = base.join(aa_agg, how='left').fillna(0)

    # Mobile features
    if not df_mob.empty:
        df_mob['recharge_amount'] = pd.to_numeric(df_mob.get('recharge_amount',0), errors='coerce').fillna(0)
        mob_agg = df_mob.groupby('beneficiary_id')['recharge_amount'].agg(['sum','mean']).rename(columns={'sum':'mob_total_recharge','mean':'mob_avg_recharge'})
        base = base.join(mob_agg, how='left').fillna(0)

    # Electricity features
    if not df_elec.empty:
        df_elec['bill_amount'] = pd.to_numeric(df_elec.get('bill_amount',0), errors='coerce').fillna(0)
        elec_agg = df_elec.groupby('beneficiary_id')['bill_amount'].agg(['sum','mean']).rename(columns={'sum':'elec_total','mean':'elec_avg'})
        base = base.join(elec_agg, how='left').fillna(0)

    base.fillna(0, inplace=True)
    return base

# ---------------- Train Model ----------------
def train_model(df, config):
    y = df['target_default'].values
    X = df.drop(columns=['target_default'])

    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    model = lgb.LGBMClassifier(**config['lgb_params'])
    model.fit(X_imputed, y)

    ensure_dir(config['model_dir'])
    joblib.dump(model, os.path.join(config['model_dir'],'lgb_model.pkl'))
    joblib.dump(imputer, os.path.join(config['model_dir'],'imputer.pkl'))
    print("Model and imputer saved.")

# ---------------- Score Model ----------------
def score_model(df, config, output='scored_output.csv'):
    model_path = os.path.join(config['model_dir'],'lgb_model.pkl')
    imputer_path = os.path.join(config['model_dir'],'imputer.pkl')
    if not os.path.exists(model_path) or not os.path.exists(imputer_path):
        raise FileNotFoundError("Model or imputer not found. Train the model first.")

    model = joblib.load(model_path)
    imputer = joblib.load(imputer_path)

    ids = df.index
    X = imputer.transform(df.drop(columns=['target_default'], errors='ignore'))
    preds = model.predict_proba(X)[:,1]

    out = pd.DataFrame({'beneficiary_id': ids, 'default_prob': preds})
    out.to_csv(output, index=False)
    print(f"Scored CSV saved at {output}")

# ---------------- Main ----------------
def main(mode='train', output=None):
    print(f"Running in {mode} mode")
    df = build_features(CONFIG)
    if mode=='train':
        train_model(df, CONFIG)
    elif mode=='score':
        score_model(df, CONFIG, output=output or 'scored_output.csv')
    else:
        raise ValueError("Mode must be 'train' or 'score'")

# ---------------- Example Jupyter usage ----------------
# main(mode='train')
# main(mode='score', output='my_score.csv')