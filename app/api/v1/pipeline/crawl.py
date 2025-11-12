from pytrends import dailydata

def crawl_daily_trends(date):
    year = date.year
    month = date.month
    day = date.day
    pytrends = dailydata.get_daily_data(
        word='',
        start_year=year,
        start_mon=month,
        stop_year=year,
        stop_mon=month,
        geo='US',
        verbose=False,
        wait_time=0
    )
    trends = pytrends.get_data()
    return trends

if __name__ == "__main__":
    import datetime
    date = datetime.date(2024, 6, 1)
    trends = crawl_daily_trends(date)
    #write to csv
    trends.to_csv(f"daily_trends_{date}.csv")