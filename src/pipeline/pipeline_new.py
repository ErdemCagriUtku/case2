from lib2to3.main import diff_texts
from typing import final

import config.config
from src.ingestion.load_new_data import load_new_data
from src.data_preparation.pre_process import pre_process

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

from src.model.predict import predict_next_year
from src.model.train_model import train_model

#!#data_valid csv test

loaded_data_array=load_new_data(config.config.PRODUCT_PATH, config.config.CUSTOMER_PATH, config.config.TRANSACTIONS_PATH)

product_df=loaded_data_array[0]
customer_df=loaded_data_array[1]
transactions_df=loaded_data_array[2]

#!#data valid other tests

# loaded_data_array=format_data(product_df, customer_df, transactions_df)
#
# product_df=loaded_data_array[0]
# customer_df=loaded_data_array[1]
# transactions_df=loaded_data_array[2]

model_df=pre_process(transactions_df, customer_df, product_df)

final_reg_model=train_model(model_df,config.config.LAST_YEAR)

pred_df=predict_next_year(model_df,final_reg_model,config.config.LAST_YEAR+1)

pred_df.to_csv(config.config.SAVE_PREDS_PATH, index=False)

# MESELELER
#
# 1) join lerken ki year ve pr code, year ve customer code unique degil, uniquelestirilmesi lazim
# 2) modeli kurarken büyük bir granularity yaptim, ama sonuc bu granularitede degil, bu mantikli mi
# 3) predict yaparken direkt bütün eski data setini ayniymis gibi kabul ettim (sales volume leri de dahil), bu mantikli mi?
# 4) gelen kodu hic test etmedim (data validation kismi)
# **5) kodumun tamami ayni sayfada structure edilmesi lazim (fonksiyonlar vs olusturulmasi lazim)
# **6) pipeline dizayninin ne oldugunu tam olarak anlayip ona uygun bir sey yaptigimdan emin olmam lazim
# 7) laso ve ridge regressionlarin parametrelerini baska sayilarla denemedim, optimize edilmesi gerekebilir
# 8) Cocuka mail atip, yarim saat schedule etmem lazim
# 9) Umut, rabia veya harunla konusmam lazim bu olmus mu diye
# 10) kodumu anlatan basit bir görsel hazirlamam lazim
# 11) en son kodumu temizlemem lazim


