# Extreme indices functions

# count of number of days Tmin (ds) is less than 0C
def frostdays(ds_Tmin, time_group):

    """ Extreme index: Frost Days - count of number of days Tmin (ds) is less than 0C.
        
        Args:
        ds_Tmin (xarray): data set of minimum temperature (Tmin)
        time_group (string): group data by time_group (e.g. 'M', 'Y') 
    """
    count_FD = ds_Tmin.where(ds_Tmin<2).resample(time = time_group).count(dim = 'time')  

    return count_FD


# count of number of days when Tmax is greater than 25C
def summerdays(ds_Tmax, time_group):
    
    """ Extreme index: Summer Days - count of number of days Tmax (ds) is greater than 25C.
        
        Args:
        ds_Tmax (xarray): data set of maximum temperature (Tmax)
        time_group (string): group data by time_group (e.g. 'M', 'Y')
    """
    count_SU = ds_Tmax.where(ds_Tmax>25).resample(time = time_group).count(dim = 'time')

    return count_SU


# count of number of days Tmax (ds) is less than 0C
def icingdays(ds_Tmax, time_group):

    """ Extreme index: Icing Days - count of number of days Tmax (ds) is less than 0C.
        
        Args:
        ds_Tmax (xarray): data set of maximum temperature (Tmax)
        time_group (string): group data by time_group (e.g. 'M', 'Y')

    """
    count_ID = ds_Tmax.where(ds_Tmax<0).resample(time = time_group).count(dim = 'time')

    return count_ID


# count of number of days Tmin (ds) is greater than 20C
def tropicalnights(ds_Tmin, time_group):

    """ Extreme index: Tropical Nights - count of number of days Tmin (ds) is greater than 20C.
        
        Args:
        ds_Tmin (xarray): data set of minimum temperature (Tmin)
        time_group (string): group data by time_group (e.g. 'M', 'Y') 
    """
    count_TR = ds_Tmin.where(ds_Tmin>20).resample(time = time_group).count(dim = 'time')

    return count_TR


# maximum daily maximum temperature each month 
def T_maxmax(ds_Tmax, time_group):

    """ Extreme index: TXx - maximum of daily maximum temperature each month
        
        Args:
        ds_Tmax (xarray): data set of maximum temperature (Tmax)
        time_group (string): group data by time_group (e.g. 'M') 
    """
    #group data by month - find max each month
    TXx = ds_Tmax.resample(time=time_group).max(dim='time')

    return TXx


# maximum daily minimum temperature each month 
def T_maxmin(ds_Tmin, time_group):    

    """ Extreme index: TNx - maximum daily minimum temperature each month 
        
        Args:
        ds_Tmin (xarray): data set of minimum temperature (Tmin)
        time_group (string): group data by time_group (e.g. 'M') 
    """
    #group data by month - find max each month
    TNx =  ds_Tmin.resample(time=time_group).max(dim='time')

    return TNx


# minimum daily minimum temperature each month 
def T_minmin(ds_Tmin, time_group):
    """ Extreme index: TNn - minimum daily minimum temperature each month 
        
        Args:
        ds_Tmin (xarray): data set of minimum temperature (Tmin)
        time_group (string): group data by time_group (e.g. 'M') 
    """
    #group data by month - find min each month
    TNn = ds_Tmin.resample(time=time_group).min(dim='time')

    return TNn


# minimum daily maximum temperature each month 
def T_minmax(ds_Tmax, time_group):

    """ Extreme index: TXn - minimum of daily maximum temperature each month
        
        Args:
        ds_Tmax (xarray): data set of maximum temperature (Tmax)
        time_group (string): group data by time_group (e.g. 'M') 
    """    
    #group data by month - find min each month
    TXn = ds_Tmax.resample(time=time_group).min(dim='time')

    return TXn


# Percentage of days when TN or TX < 10th percentile 
def T_10p(dataset, time_group, start_date, end_date):
    """ Extreme index: TN10p/TX10p - percentage of days when TN or TX < 10th percentile
        
        Args:
        dataset (xarray): data set of either Tmin or Tmax
        time_group (string): group data by time_group (e.g. 'M')
        start_date (string): start date of period over which to calculate percentile
        end_date (string): end date of period over which to calculate percentile
    """    

    # find the 10th percentile
    p10 = dataset.sel(time=slice(start_date, end_date)).groupby(time_group[1]).quantile(0.1, dim=['time'])
    # group data by month - find min each month
    T_10p_count = dataset.where(dataset < p10).resample(time = time_group[0]).count(dim = 'time')
    
    # resample by month
    T_10p_count_final = month_resample(T_10p_count)
    
    # find where any NaN values occur
    NaN_ds = dataset.isnull() # listed as True if it's a NaN value
    # count the number of NaN values per month 
    NaN_count = NaN_ds.where(NaN_ds==True).resample(time = time_group[0]).count(dim = 'time')
    
    # find the no. days in each month (remembering to minus any days that have NaN values)
    mon_range = T_10p_count.time.dt.days_in_month - NaN_count

    # convert the (monthly) count of TN10p to a percentage
    T_10p = T_10p_count*100/(mon_range)  
    
    # remove the quantile dimension so I can combine datasets (ie T_90p) later
    del T_10p['quantile']

    return T_10p


# Percentage of days when TN or TX > 90th percentile 
def T_90p(dataset, time_group, start_date, end_date):
    """ Extreme index: TN90p/TX90p - percentage of days when TN or TX > 90th percentile
        
        Args:
        dataset (xarray): data set of either Tmin or Tmax
        time_group (string): group data by time_group (e.g. 'M')
        start_date (string): start date of period over which to calculate percentile
        end_date (string): end date of period over which to calculate percentile
    """    

    # find the 10th percentile
    p90 = dataset.sel(time=slice(start_date, end_date)).groupby(time_group[1]).quantile(0.9, dim=['time'])

    # group data by month - find min each month
    T_90p_count = dataset.where(dataset > p90).resample(time = time_group[0]).count(dim = 'time')
    
    # resample by month
    T_90p_count_final = month_resample(T_90p_count)
    
    # find where any NaN values occur
    NaN_ds = dataset.isnull() # listed as True if it's a NaN value
    # count the number of NaN values per month 
    NaN_count = NaN_ds.where(NaN_ds==True).resample(time = time_group[0]).count(dim = 'time')

    # find the no. days in each month (remembering to minus any days that have NaN values)
    mon_range = T_90p_count.time.dt.days_in_month - NaN_count

    # convert the (monthly) count of TN10p to a percentage
    T_90p = T_90p_count*100/(mon_range)
    
    # remove the quantile dimension so I can combine datasets (ie T_10p) later
    del T_90p['quantile']

    return T_90p


# daily temperature range 
def daily_range(ds_Tmin, ds_Tmax, time_group):

    """ Extreme index: DTR - average daily temperature range for each month (1 value per month of each year)
       
        Args:
        ds_Tmin (xarray): data set of minimum temperature (Tmax)
        ds_Tmax (xarray): data set of maximum temperature (Tmax)
        time_group (string): group data by time_group (e.g. 'M') 
    """      
    DTR = (ds_Tmax - ds_Tmin).resample(time=time_group).mean(dim='time')

    return DTR    


# extreme temperature range 
def extreme_range(ds_TNn, ds_TXx):
    
    """ Extreme index: ETR - extreme temperature range for each month (1 value per month of each year)
        
        Args:
        ds_TNn (xarray): data set of minimum temperature (Tmax)
        ds_TXx (xarray): data set of maximum temperature (Tmax)
        time_group (string): group data by time_group (e.g. 'M') 
    """  
    ETR = ds_TXx - ds_TNn
    
    return ETR


# function to calculate all extreme indices and put them in an xarray
def extreme_indices(dataset, time_group, start_date, end_date):
    
    """ Extreme indices: Calculate selected temperature extreme indices and store them in an xarray. 
        
        Args:
        dataset (xarray): data set of temperature  containing both Tmin and Tmax
        time_group (string): list of 2 strings to group data by, first input is arg for resample func (e.g. 'M'), second input is groupby arg (e.g. 'time.month')
        start_date (string): start date of period over which to calculate percentile
        end_date (string): end date of period over which to calculate percentile
    """ 
    
    import xarray as xr 
    
    # select out Tmin and Tmax from input dataset
    ds_Tmin = dataset.Tmin
    ds_Tmax = dataset.Tmax
    
    # calculate all the extreme indices needed
    FD = frostdays(ds_Tmin, time_group[0])
    SU = summerdays(ds_Tmax, time_group[0])
    ID = icingdays(ds_Tmax, time_group[0])
    TR = tropicalnights(ds_Tmin, time_group[0])
    TXx = T_maxmax(ds_Tmax, time_group[0])
    TNx = T_maxmin(ds_Tmin, time_group[0])
    TNn = T_minmin(ds_Tmin, time_group[0])
    TXn = T_minmax(ds_Tmax, time_group[0])
    TN10p = monthly_10p(ds_Tmin, start_date, end_date)
    TX10p = monthly_10p(ds_Tmax, start_date, end_date)
    TN90p = monthly_90p(ds_Tmin, start_date, end_date)
    TX90p = monthly_90p(ds_Tmax, start_date, end_date)
    DTR = daily_range(ds_Tmin, ds_Tmax, time_group[0])
    ETR = extreme_range(TNn, TXx)
    
    # put all indicies into one xarray
    indicies = xr.Dataset({'FD': FD, 'SU': SU, 'ID': ID, 'TR': TR, 'TXx': TXx, 'TNx': TNx, 'TNn': TNn, 'TXn': TXn, 'TN10p': TN10p, 'TX10p': TX10p, 'TN90p': TN90p, 'TX90p': TX90p, 'DTR': DTR, 'ETR': ETR})
    
    return indicies
 
    
# monthly 

def monthly_90p(dataset, start_date, end_date):
    """ Extreme index: TN10p/TX10p - percentage of days when TN or TX > 90th percentile
        
        Args:
        dataset (xarray): data set of either Tmin or Tmax
        start_date (string): start date of period over which to calculate percentile
        end_date (string): end date of period over which to calculate percentile
    """   
    import xarray as xr, pandas as pd
    
    # find the 90th percentile for each month
    p90 = dataset.sel(time=slice(start_date, end_date)).groupby('time.month').quantile(0.9, dim=['time'])

    ds_m = []
    ds_NaN_m = []
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # find where any NaN values occur
    NaN_ds = dataset.isnull() # listed as True if it's a NaN value
    
    # loop over 
    for m in range(1,13):
        # count number of times daily data above 90p
        count = dataset.where(dataset.sel(time=(dataset['time.month']==m)) > p90.sel(month=m)).resample(time = '12M').count(dim = 'time')
        # count the number of NaN values per month 
        count_NaN = NaN_ds.where(NaN_ds.sel(time=(dataset['time.month']==m))==True).resample(time = '12M').count(dim = 'time')
        # count number of days per months
        days_in_mon = dataset.sel(time=(dataset['time.month']==m)).time.dt.days_in_month.resample(time='12M').count(dim='time')
        # count number of days per month minus any NaN values
        mon_range = days_in_mon - count_NaN

        T_90p_count = count*100/(mon_range)
        
        # remove time and month coord
        del T_90p_count['month']
#         del T_90p_count['time']
        
        # append percentage for each month (of each year) into one ds
        ds_m.append(T_90p_count)
        
     # recombine all months into one ds and concat over month dimension
    p90_count = xr.concat(ds_m, dim = 'time', coords = 'minimal')
#     p90_count.coords['month'] = months
#     p90_count.coords['time'] = pd.date_range(str(dataset['time.year'][0].data), str(dataset['time.year'][-1].data), freq='YS')
    
    # remove the quantile dimension so I can combine datasets (ie T_10p) later
    del p90_count['quantile']
    
    return p90_count



def monthly_10p(dataset, start_date, end_date):
    """ Extreme index: TN10p/TX10p - percentage of days when TN or TX < 10th percentile
        
        Args:
        dataset (xarray): data set of either Tmin or Tmax
        start_date (string): start date of period over which to calculate percentile
        end_date (string): end date of period over which to calculate percentile
    """   
    import xarray as xr, pandas as pd
    
    # find the 10th percentile for each month
    p10 = dataset.sel(time=slice(start_date, end_date)).groupby('time.month').quantile(0.1, dim=['time'])

    ds_m = []
    ds_NaN_m = []
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    # find where any NaN values occur
    NaN_ds = dataset.isnull() # listed as True if it's a NaN value
    
    # loop over months
    for m in range(1,13):
        # count number of times daily data below 10p
        count = dataset.where(dataset.sel(time=(dataset['time.month']==m)) < p10.sel(month=m)).resample(time = '12M').count(dim = 'time')
        # count the number of NaN values per month 
        count_NaN = NaN_ds.where(NaN_ds.sel(time=(dataset['time.month']==m))==True).resample(time = '12M').count(dim = 'time')
        # count number of days per months
        days_in_mon = dataset.sel(time=(dataset['time.month']==m)).time.dt.days_in_month.resample(time='12M').count(dim='time')
        # count number of days per month minus any NaN values
        mon_range = days_in_mon - count_NaN

        T_10p_count = count*100/(mon_range)
        
        # remove time and month coord
        del T_10p_count['month']
#         del T_10p_count['time']
        
        # append percentage for each month (of each year) into one ds
        ds_m.append(T_10p_count)
        
     # recombine all months into one ds and concat over month dimension
    p10_count = xr.concat(ds_m, dim = 'time', coords = 'minimal')
#     p10_count.coords['month'] = months
#     p10_count.coords['time'] = pd.date_range(str(dataset['time.year'][0].data), str(dataset['time.year'][-1].data), freq='YS')
    
    # remove the quantile dimension so I can combine datasets (ie T_10p) later
    del p10_count['quantile']
    
    return p10_count
    
    
# Percentage of days when TN or TX < 10th percentile by season
def seasonal_10p(dataset, start_date, end_date):
    """ Extreme index: TN10p/TX10p - percentage of days when TN or TX < 10th percentile
        
        Args:
        dataset (xarray): data set of either Tmin or Tmax
        start_date (string): start date of period over which to calculate percentile
        end_date (string): end date of period over which to calculate percentile
    """    
    
    # first I need to define a new coordinate (seasonyear) so that december gets counted with the adjoining jan and feb
    seasonyear = (dataset.time.dt.year + (dataset.time.dt.month//12)) 
    dataset.coords['seasonyear'] = seasonyear
    
    # find the 10th percentile
    p10 = dataset.sel(time=slice(start_date, end_date)).groupby('time.season').quantile(0.1, dim=['time'])
    
    # group data by month - find min each month
    T_10p_count = dataset.where(dataset < p10).resample(time = 'QS-DEC').count(dim = 'time')
    
    # resample by season
    T_10p_count_final = season_resample(T_10p_count)
    
    # find where any NaN values occur
    NaN_ds = dataset.isnull() # listed as True if it's a NaN value
    # count the number of NaN values per year 
    NaN_count = NaN_ds.where(NaN_ds==True).resample(time = 'M').count(dim = 'time')
    # find the no. days in each month (remembering to minus any days that have NaN values)
    mon_range = dataset.time.dt.days_in_month - NaN_count
    # resample and sum months in each quarter to find the no. days in each season
    season_range = mon_range.resample(time = 'QS-DEC').sum()
    # resample NaN values by season
    season_range_final = season_resample(season_range)
    
    # convert the (seasonal) count of TN10p to a percentage
    T_10p = T_10p_count_final*100/(season_range_final)
    # add the time/seasonyear dimension back in 
    # (since daily data take every 365th entry so i get one value for each year and excelude last year)
    T_10p.coords['seasonyear'] = seasonyear[:-365].isel(time=slice(0,None,365))
    
    # remove the quantile dimension so I can combine datasets (ie T_90p) later
    del T_10p['quantile']
    
    return T_10p 
    
    
# Percentage of days when TN or TX > 90th percentile by season
def seasonal_90p(dataset, start_date, end_date):
    """ Extreme index: TN90p/TX90p - percentage of days when TN or TX > 90th percentile
        
        Args:
        dataset (xarray): data set of either Tmin or Tmax
        start_date (string): start date of period over which to calculate percentile
        end_date (string): end date of period over which to calculate percentile
    """ 
    
    # first I need to define a new coordinate (seasonyear) so that december gets counted with the adjoining jan and feb
    seasonyear = (dataset.time.dt.year + (dataset.time.dt.month//12)) 
    dataset.coords['seasonyear'] = seasonyear
        
    # perform an operation
    p90 = dataset.sel(time=slice(start_date, end_date)).groupby('time.season').quantile(0.9, dim=['time'])
    
    # group data by season - find count for each season
    T_90p_count = dataset.where(dataset > p90).resample(time='QS-DEC').count(dim = 'time')
    
    # resample by season
    T_90p_count_final = season_resample(T_90p_count)
    
    # find where any NaN values occur
    NaN_ds = dataset.isnull() # listed as True if it's a NaN value
    # count the number of NaN values per year 
    NaN_count = NaN_ds.where(NaN_ds==True).resample(time = 'M').count(dim = 'time')
    # find the no. days in each month (remembering to minus any days that have NaN values)
    mon_range = dataset.time.dt.days_in_month - NaN_count
    # resample and sum months in each quarter to find the no. days in each season
    season_range = mon_range.resample(time = 'QS-DEC').sum()
    # resample NaN values by season
    season_range_final = season_resample(season_range)
    
    # convert the (seasonal) count of TN10p to a percentage
    T_90p = T_90p_count_final*100/(season_range_final)
    # add the time/seasonyear dimension back in 
    # (since daily data take every 365th entry so i get one value for each year and excelude last year)
    T_90p.coords['seasonyear'] = seasonyear[:-365].isel(time=slice(0,None,365))
    
    # remove the quantile dimension so I can combine datasets (ie T_90p) later
    del T_90p['quantile']
    
    return T_90p


# function to resample data by season (since python resample fucntion does'nt do this automatically!!)
# this function is called in the quantile functions above 
def season_resample(dataset):
    import xarray as xr
    
    seasons = ['DJF', 'MAM', 'JJA', 'SON']
    dataset_s = []
    for i, s in enumerate(seasons):
        
        # check if ds has 'season' dim
        if hasattr(dataset, 'season'):
            # select out each season into an array
            ds_season = dataset.isel(time=slice(i,None,4)).sel(season=s)
            # remove season dimension so can create correct new season dim later
            del ds_season['season']
            
        else:
            # select out each season into an array
            ds_season = dataset.isel(time=slice(i,None,4))
        
        # remove time dimension
        del ds_season['time']

        # remove the last december from season so each season has the same number of timesteps
        if i == 0:
            ds_season = ds_season.sel(time=ds_season.time[:-1])

        # append each season to one 
        dataset_s.append(ds_season)

    # recombine all seasons into one ds and concat over season dimension
    ds_final = xr.concat(dataset_s, dim = 'season', coords = 'minimal')
    ds_final.coords['season'] = seasons
    
    return ds_final

# function to resample data by month (since python resample fucntion does'nt do this automatically!!)
# this function is called in the quantile functions above 
def month_resample(dataset):
    import xarray as xr
    
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    dataset_m = []
    for i, m in enumerate(months):
        
        # check if ds has 'month' dim
        if hasattr(dataset, 'month'):
            # select out each season into an array
            ds_month = dataset.isel(time=slice(i,None,12)).sel(month=m)
            # remove season dimension so can create correct new season dim later
            del ds_month['month']
            
        else:
            # select out each month into an array
            ds_month = dataset.isel(time=slice(i,None,12))
        
        # remove time dimension
        del ds_month['time']

        # remove the last december from season so each season has the same number of timesteps
#         if i == 0:
#             ds_month = ds_month.sel(time=ds_month.time[:-1])

        # append each month to one 
        dataset_m.append(ds_month)

    # recombine all months into one ds and concat over season dimension
    ds_final = xr.concat(dataset_m, dim = 'month', coords = 'minimal')
    ds_final.coords['month'] = months
    
    return ds_final


# daily temperature range by season
def seasonal_DTR(ds_Tmin, ds_Tmax):

    """ Extreme index: DTR - average daily temperature range for each season (1 value per season)
       
        Args:
        ds_Tmin (xarray): data set of minimum temperature (Tmax)
        ds_Tmax (xarray): data set of maximum temperature (Tmax)
    """      
    # first I need to define a new coordinate (seasonyear) so that december gets counted with the adjoining jan and feb
    seasonyear = (ds_Tmin.time.dt.year + (ds_Tmin.time.dt.month//12)) 
    ds_Tmin.coords['seasonyear'] = seasonyear
    
    # calculate teh daily temp range for each quarter (season)
    DTR = (ds_Tmax - ds_Tmin).resample(time='QS-DEC').mean(dim='time')
    
    # resample by season
    DTR_final = season_resample(DTR)
    # add the time/seasonyear dimension back in 
    # (since daily data take every 365th entry so i get one value for each year and excelude last year)
#     DTR_final.coords['seasonyear'] = seasonyear[:-364].isel(time=slice(0,None,365))
    DTR_final.coords['seasonyear'] = seasonyear[:-366].isel(time=slice(0,None,365))
    

    return DTR_final 


    
    





