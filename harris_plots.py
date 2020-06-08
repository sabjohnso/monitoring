
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import data


def delta(u):
    return u[1:]-u[:-1]



class HarrisCountyPlotter(object):
    pattern = "Harris, Texas, US"
    dt = datetime.timedelta(days = 0.5)

    start = 60
    def __init__(self, reports):
        self.dates = np.array(reports.dates)
        self.indices = np.array([i for i in range( len( reports.dates ))])
        self.__getDeaths( reports )
        self.__getConfirmed( reports )

    def __getDeaths(self, reports):
        self.deaths = reports.filteredDeaths( data.regexPredicate( self.pattern ))

    def __getConfirmed(self, reports):
        self.confirmed = reports.filteredConfirmed( data.regexPredicate( self.pattern ))

    def plotConfirmed(self):
        fig, axes = plt.subplots(nrows = 2, sharex = True)
        axes[0].grid(True)
        axes[1].grid(True)
        axes[0].set_title('Harris County COVID-19 Cases')        
        self.__cumulativeConfirmed(axes[0])
        self.__deltaConfirmed(axes[1])
        axes[1].format_xdata = mdates.DateFormatter('%Y-%m-%d')
        fig.autofmt_xdate()
        plt.show()

    def plotDeaths(self):
        fig, axes = plt.subplots(nrows = 2, sharex = True)
        axes[0].grid(True)
        
        axes[1].grid(True)
        axes[0].set_title('Harris County COVID-19 Deaths')
        self.__cumulativeDeaths(axes[0])
        self.__deltaDeaths(axes[1])

        axes[1].format_xdata = mdates.DateFormatter('%Y-%m-%d')
        fig.autofmt_xdate()

        plt.show()

    def plot(self, filename = None):
        fig, axes = plt.subplots(nrows = 2, sharex = True)
        axes[0].grid(True)
        axes[1].grid(True)
        axes[0].set_title('Harris County COVID-19 Cases and Deaths')        
        self.__cumulative(axes[0])
        self.__delta(axes[1])

        axes[1].format_xdata = mdates.DateFormatter('%Y-%m-%d')
        fig.autofmt_xdate()
        
        plt.show()

    #
    # ... Cumulative Data
    #
    def __cumulative(self, ax1):
        ax2 = ax1.twinx()
        self.__cumulativeConfirmed(ax1)
        self.__cumulativeDeaths(ax2)

    def __cumulativeConfirmed(self, ax):
        color = 'tab:blue'
        ax.set_ylabel('Cumulative Cases', color = color)
        ax.plot(self.dates[self.start:], self.confirmed[self.start:], color = color)
        ax.tick_params(axis='y', labelcolor=color)

    def __cumulativeDeaths(self, ax):
        color = 'tab:red'
        ax.set_ylabel('Cumulative Deaths', color = color)
        ax.plot(self.dates[self.start:], self.deaths[self.start:], color = color)
        ax.tick_params(axis='y', labelcolor=color)

    #
    # ... Daily Changes
    #
    def __delta(self, ax1):
        ax2 = ax1.twinx()
        self.__deltaConfirmed(ax1)
        self.__deltaDeaths(ax2)

    def __deltaConfirmed(self, ax):
        color = 'tab:blue'
        ax.set_xlabel('Date')
        ax.set_ylabel('New Cases', color = color)
        ax.bar(self.dates[self.start:]+self.dt/2, delta(self.confirmed)[self.start-1:], self.dt, color = color)
        ax.tick_params(axis='y', labelcolor = color)

    def __deltaDeaths(self, ax):
        color = 'tab:red'
        ax.set_xlabel('Date')
        ax.set_ylabel('New Deaths', color = color)
        ax.bar(self.dates[self.start:]-self.dt/2, delta(self.deaths)[self.start-1:], self.dt, color = color)
        ax.tick_params(axis='y', labelcolor = color)
    




