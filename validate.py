import os 
import shutil
from datetime import datetime as dt
import pandas as pd
date = dt.today().strftime('%Y%m%d')
os.chdir(f'D:\\Python\\Project')
master = pd.read_csv('product_master.csv')
os.chdir(f'D:\\Python\\Project\\incoming_files\\{date}')
date1 = dt.today().strftime(('%d-%m-%Y'))
datef =dt.today().date()
rejection_path = f'D:\\Python\\Project\\rejected_files\\{date}'
file_path= f'D:\\Python\\Project\\incoming_files\\{date}'
pas = True
def validate_file(file,passed,failed):

    order  = pd.read_csv(f'D:\\Python\\Project\\incoming_files\\{date}\\{file}')

    #product ID check
    oProductId = list(order['product_id'])
    mProductId = list(master['product_id'])
    a = True
    j=0
    r =1
    for i in oProductId:
        if i in mProductId:
            j+=1
            continue
        else:
            os.makedirs(rejection_path,exist_ok= True)
            a=False
            error = order.loc[[j]].copy()
            error['error reason'] = ['product Id is not pressent in master file']
            error.to_csv(f'{rejection_path}\\error_order_product_id_{r}.csv',index=False)
            j+=1
            r+=1
            print(f"{i} productId not present in master file, file move to rejected folder.")
                
        
    if a==False:
        print("product ID in orders file is not present in master file!!!!")
        global pas
        pas =False
    
    #order date check
    a=True
    j=0
    r =1
    for i in order["order_date"]:
        i = dt.strptime(i, '%d-%m-%Y').date()
        if i >datef:
            os.makedirs(rejection_path,exist_ok=True)
            error = order.loc[[j]].copy()  
            error['error reason'] = ['Order date is in future']
            error.to_csv(f'{rejection_path}\\error_order_order_date_{r}.csv',index=False)
            
            a= False
            j+=1
            r+=1
        else:
            j+=1
            continue
    if a== False:
        print("Future order date found!!!! ")
        pas = False

    #sale column check
    mergedDF = pd.merge(order,master,on = 'product_id')
    mergedDF['multiply'] = mergedDF['quantity']*mergedDF['price']
    mergedDF["equal"]  =mergedDF['multiply'] == mergedDF['sales']
    a=True
    j =0 
    r=1
    for i in mergedDF['equal']:
        if i == True:
            j+=1
            continue
        else:
            os.makedirs(rejection_path,exist_ok= True )
            a=False
            error = order.iloc[[j]].copy()
            error['error reason'] = ['sales value is mismatching']
            error.to_csv(f'{rejection_path}\\error_sales_column_{r}.csv',index=False)
            j+=1
            r+=1
    if a ==False:
        print("error with sales column!!!!!")
        pas = False

    #null avlue 
    orderdf = order.isna()
    a= True
    r=1
    for  i in range(len(order)):
        for j in range(int(order.shape[1])):
            if orderdf.iloc[i,j] == True:
                os.makedirs(rejection_path,exist_ok= True )
                error =order.iloc[[i]].copy()
                error['error reason'] = 'Null value found'
                error.to_csv(f'{rejection_path}\\error_null_value_{r}.csv',index=False)
                r+=1
                a= False    
    if a ==False:
        print("null value found")
        pas = False

    #location check
    l1 = list(order['city'].str.lower())
    a= True
    j=0
    r=1
    for i in l1:
        if i != 'mumbai' and i!='bangalore':
            os.makedirs(rejection_path,exist_ok= True )
            a= False 
            error = order.loc[[j]].copy()
            error['error reason'] = ['Location invalid']
            error.to_csv(f'{rejection_path}\\error_Location_invalid_{r}.csv',index=False)
            j+=1
            r+=1
            
        else:
             j+=1
             continue        
    if a ==False:
        print("Invalid Location found!!!!! ")
        pas = False


    
    


    if pas ==False:
        print(f"{file} is rejected!! ")
        shutil.copy(f'{file_path}\\{file}',rejection_path)
        return passed  , failed +1
    
    else:
        shutil.copy(f'{file_path}\\{file}','D:\Python\Project\successful_files')
        return passed+1, failed
        