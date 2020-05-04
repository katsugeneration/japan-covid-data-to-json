import pathlib
import pandas as pd
import datetime
import matplotlib.dates
from matplotlib import pyplot as plt

df_p = pd.read_csv('https://dl.dropboxusercontent.com/s/6mztoeb6xf78g5w/COVID-19.csv', header=0)
df_pn = df_p.pivot_table(
    values='人数',
    index=pd.DatetimeIndex(pd.to_datetime(df_p['確定日'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')),
    columns='受診都道府県',
    aggfunc='sum',
    fill_value=0)
weekly = pd.Grouper(freq='W-MON', label='left')
df_p_week = df_pn.groupby(weekly).sum()

df = pd.read_csv('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=911a386b6c9c230f', header=0)
df['date'] = pd.to_datetime(df['date'])
df['sub_region_1'] = df['sub_region_1'].fillna('')
df['sub_region_2'] = df['sub_region_2'].fillna('')

weekly = pd.Grouper(key='date', freq='W-MON', label='left')
df_agg = df.groupby([
        'country_region',
        'sub_region_1',
        'sub_region_2',
        weekly]).mean()

dates = df_agg.index.get_level_values('date')
_df_p_week = df_p_week.loc[dates[0]:dates[-1] + datetime.timedelta(days=7)]
dates = _df_p_week.index.to_list()

regions = {
    'Hokkaido': '北海道',
    'Aomori': '青森県',
    'Iwate': '岩手県',
    'Miyagi': '宮城県',
    'Akita': '秋田県',
    'Yamagata': '山形県',
    'Fukushima': '福島県',
    'Ibaraki': '茨城県',
    'Tochigi': '栃木県',
    'Gunma': '群馬県',
    'Saitama': '埼玉県',
    'Chiba': '千葉県',
    'Tokyo': '東京都',
    'Kanagawa': '神奈川県',
    'Yamanashi': '山梨県',
    'Nagano': '長野県',
    'Niigata': '新潟県',
    'Toyama': '富山県',
    'Ishikawa': '石川県',
    'Fukui': '福井県',
    'Shizuoka': '静岡県',
    'Aichi': '愛知県',
    'Gifu': '岐阜県',
    'Mie': '三重県',
    'Shiga': '滋賀県',
    'Kyoto': '京都府',
    'Osaka': '大阪府',
    'Hyogo': '兵庫県',
    'Nara': '奈良県',
    'Wakayama': '和歌山県',
    'Tottori': '鳥取県',
    'Shimane': '島根県',
    'Okayama': '岡山県',
    'Hiroshima': '広島県',
    'Yamaguchi': '山口県',
    'Tokushima': '徳島県',
    'Kagawa': '香川県',
    'Ehime': '愛媛県',
    'Kochi': '高知県',
    'Fukuoka': '福岡県',
    'Saga': '佐賀県',
    'Nagasaki': '長崎県',
    'Kumamoto': '熊本県',
    'Oita': '大分県',
    'Miyazaki': '宮崎県',
    'Kagoshima': '鹿児島県',
    'Okinawa': '沖縄県'
}

for k, v in regions.items():
    df_region = df_agg.xs([k], level=['sub_region_1'])
    fig = plt.figure(figsize=(16.0, 9.0))
    ax1 = fig.subplots()
    ax2 = ax1.twinx()

    if v not in _df_p_week.columns:
        _df_p_week[v] = 0

    ax1.bar(dates, _df_p_week[v], color='y', width=2.0, label='新規感染判明数')
    ax2.plot(dates[:-1], df_region['workplaces_percent_change_from_baseline'], marker='o', label='職場滞在指数')
    ax2.plot(dates[:-1], df_region['transit_stations_percent_change_from_baseline'], marker='o', label='公共交通機関滞在指数（電車、バス、など）')
    ax2.plot(dates[:-1], df_region['parks_percent_change_from_baseline'], marker='o', label='公園滞在指数（公園、海、など）')
    ax2.plot(dates[:-1], df_region['grocery_and_pharmacy_percent_change_from_baseline'], marker='o', label='食料品・薬局滞在指数（スーパー、食料品店、薬局、など） ')
    ax2.plot(dates[:-1], df_region['retail_and_recreation_percent_change_from_baseline'], marker='o', label='小売・商業施設滞在指数（飲食店、ショッピングセンター、遊園地、美術館、図書館、映画館、など）')

    ax1.xaxis.set_major_locator(matplotlib.dates.WeekdayLocator(byweekday=0, interval=1))
    ax1.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax1.set_ylabel('新規感染判明数（人）', fontname='IPAGothic', fontsize=15)
    ax2.set_ylabel('2020年1月からの変化率（%）', fontname='IPAGothic', fontsize=15)
    fig.autofmt_xdate(rotation=90)
    fig.legend(loc='upper left', prop={'family': 'IPAGothic', 'size': 15})
    fig.savefig('moving_images/%s.png' % v)
