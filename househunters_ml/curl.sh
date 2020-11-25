curl -X POST -d '{
"LivingArea_m2":90,
"QuietRoad":1,
"Num_Bedrooms":3,
"StatusRank":2233,
"Avg_house_value_WOZ_1000euros":600,
"Avg_WOZ_m2":60,
"CitySide":1,
"HouseType_Detached":0,
"Age_cat_Before_war":0,
"Urbanity_class_5":1
}' http://127.0.0.1:5008/predict



'LivingArea_m2', 'QuietRoad', '#Bedrooms', 'StatusRank',
       'Avg_house_value_WOZ_1000euros', 'Avg_WOZ_m2', 'CitySide',
       'HouseType_Detached', 'Age_cat_Before war', 'Urbanity_class_5'

'LivingArea_m2', 'QuietRoad', '#Bedrooms', 'StatusRank',
       'Avg_house_value_WOZ_1000euros', 'Avg_WOZ_m2', 'CitySide',
       'HouseType_Detached', 'Age_cat_Before war', 'Urbanity_class_5'


http://127.0.0.1:5008/url_prediction?LivingArea_m2=90&QuietRoad=1&Num_Bedrooms=3&StatusRank=2233&Avg_house_value_WOZ_1000euros=600&Avg_WOZ_m2=60&CitySide=1&HouseType_Detached=0&Age_cat_Before_war=0&Urbanity_class_5=1