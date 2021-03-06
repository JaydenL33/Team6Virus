import matplotlib.pyplot as plt
import pandas as pd
import pickle
import numpy as np
import seaborn as sn

# Python CORE
import os
import pickle
from datetime import datetime

# DATA MANIP: PANDAS AND NUMPY
import pandas as pd
import numpy as np

# SEABORN
import seaborn as sns

# MATPLOTLIB
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def groupbyMonthlyCovid(df):
	"""
	Author: Albert Ferguson
	Reindex for time by retyping and applying a PeriodIndex selecting the M (mnonthly) opt.
	Use the groupby function of a dataframe and the column we want to groupby, return a sum
	"""

	# convert to PeriodIndexing
	try:
		df.dateRep = pd.to_datetime(df.dateRep)
		df = df.groupby(pd.PeriodIndex(df.dateRep, freq = "M"), axis = 0).sum()

	except AttributeError:
		df.index = pd.to_datetime(df.index)
		df = df.groupby(pd.PeriodIndex(df.index, freq = "M"), axis = 0).sum()


		# DOESN'T WORK
	# re add the schema
	df["schema"] = "COVID19"

	return df.reset_index()

def groupbyDailyCovid(df):
	"""
	Author: Albert Ferguson
	Reindex for time by retyping and applying a PeriodIndex selecting the M (mnonthly) opt.
	Use the groupby function of a dataframe and the column we want to groupby, return a sum
	"""
	# convert to PeriodIndexing
	try:
		df.dateRep = pd.to_datetime(df.dateRep)
		df = df.groupby(pd.PeriodIndex(df.dateRep, freq = "D"), axis = 0).sum()
		df = df.to_timestamp() # convert from PeriodIndex to DatetimeIndex

	except AttributeError:
		df.index = pd.to_datetime(df.index)
		df = df.groupby(pd.PeriodIndex(df.index, freq = "D"), axis = 0).sum()
		df = df.to_timestamp()
	
	else:
		# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html?highlight=dt#pandas.Series.dt
		# series objects of datetime can use dt accessor, see link above.
		# add a string rep for graphing labels
		df["dateRep_str"] = df.index.strftime("%Y-%m-%d")
		# df.dateRep_str = [datetime.strptime(d, "%Y-%m-%d") for d in df.dateRep_str]
		# re add the schema
		df["schema"] = "COVID19"
		df = df.reset_index()
		
	return df

def groupbyCountry(df):
	"""
	Author: Albert Ferguson
	Use the groupby function of a dataframe and the column we want to groupby, return a sum
	Note: this differs from df to df as schema may change and the field for countries is labelled
		differently.
	"""

	# aggregate for countriesAndTerritories data
	# save the schema for re adding later..TODO: figure out non destructive method
	schema_str = df.schema[0]

	try:
		df = df.groupby(df.countriesAndTerritories, axis = 0).sum()
		df = df.reset_index()

	except AttributeError:
		try:
			df = df.groupby(df.COUNTRY, axis = 0).sum()
			df = df.reset_index()

		except AttributeError:
			pass

	# re add the schema
	df["schema"] = schema_str
	return df

def dateconv(df11):
	# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.html?highlight=dt#pandas.Series.dt
	# series objects of datetime can use dt accessor, see link above.
	df11.dateRep = df11.dateRep.dt.strftime("%Y-%m-%d")
	df11.dateRep = [datetime.strptime(d, "%Y-%m-%d") for d in df11.dateRep]

def setupTL(df11):

	numPoints = int(len(df11.cases)/7)
	# y_repeatMat = [-7, 7, -5, 5, -3, 3, -1, 1]
	y_cases = df11.cases
	# levels = np.tile(y_repeatMat, numPoints)
	# index the levels list
	# levels = levels[:len(df11.dateRep)]
	fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
	
	markerline, stemline, baseline = ax.stem(df11.dateRep, y_cases,
                                         linefmt="C3-", basefmt="k-",
                                         use_line_collection=True)

	plt.setp(markerline, mec="k", mfc="w", zorder=3)

	markerline.set_ydata(np.zeros(len(df11.dateRep)))

	# annotate lines
	vert = np.array(['top', 'bottom'])[(y_cases > 0).astype(int)]
	for d, l, r, va in zip(df11.dateRep, y_cases, df11.countriesAndTerritories, vert):
	    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
	                textcoords="offset points", va=va, ha="right")

	# format xaxis with 4 month intervals
	#ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=4))
	ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
	plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
	
	# formatting
	ax.set(title="COVID19 dates")
	ax.margins(y=0.1)
	# remove y axis and spines
	ax.get_yaxis().set_visible(False)
	for spine in ["left", "top", "right"]:
	    ax.spines[spine].set_visible(False)

	plt.show()

def setupTLGlobal(df11):
	y_cases = df11.cases
	y_deaths = df11.deaths
	fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
	
	markerline, stemline, baseline = ax.stem(df11.dateRep, y_cases,
                                         linefmt="C3-", basefmt="k-",
                                         use_line_collection=True)

	plt.setp(markerline, mec="k", mfc="w", zorder=3)

	markerline.set_ydata(np.zeros(len(df11.dateRep)))

	# annotate lines
	vert = np.array(['top', 'bottom'])[(y_cases > 0).astype(int)]
	for d, l, r, va in zip(df11.dateRep, y_cases, df11.dateRep_str, vert):
	    ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
	                textcoords="offset points", va=va, ha="right")

	# format xaxis with 4 month intervals
	#ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%b %Y"))
	plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
	
	# formatting
	ax.set(title="COVID19 New Cases Global vs. Time")
	ax.margins(y=0.1)
	# remove y axis and spines
	ax.get_yaxis().set_visible(False)
	for spine in ["left", "top", "right"]:
	    ax.spines[spine].set_visible(False)

	plt.show()


with open(os.path.join(os.pardir, "processing_dump.txt"), "rb") as f:
		df_list = pickle.load(f)
		df = df_list

# first 10?? Cool idea
df11 = df_list[-1]
dfDailyGlobal = groupbyDailyCovid(df11)
setupTL(df11)
setupTLGlobal(dfDailyGlobal)
