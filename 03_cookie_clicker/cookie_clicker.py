"""
Cookie Clicker Simulator
"""
import math
import simpleplot
import random
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 1000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        final_time = "\nTime: " + str(self._time)
        final_cookies = "\nCurrent_Cookies: " + str(self._current_cookies)
        cps = "\nCPS: " + str(self._cps)
        total_cookies = "\nTotal Cookies: " + str(self._total_cookies)
        history = self.get_history()
        history_length = len(history)
        formatted_history = "\nHistory (length: " + str(history_length) + "):" + str(history)

        return final_time + final_cookies + cps + total_cookies + formatted_history

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies < self._current_cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookies) / self._cps)

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            income = time * self._cps
            self._current_cookies += income
            self._total_cookies += income
            self._time += time


    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    build_state = build_info.clone()
    click_state = ClickerState()

    while click_state.get_time() <= duration:
        time_left = duration - click_state.get_time()
        next_purchase = strategy(click_state.get_cookies(),
                                 click_state.get_cps(),
                                 click_state.get_history(),
                                 time_left,
                                 build_state)

        if next_purchase == None:
            click_state.wait(time_left)
            break

        item_cost = build_state.get_cost(next_purchase)

        time_needed = click_state.time_until(item_cost)

        if time_needed > time_left:
            click_state.wait(time_left)
            break

        click_state.wait(time_needed)

        click_state.buy_item(next_purchase, item_cost, build_state.get_cps(next_purchase))
        build_state.update_item(next_purchase)

    return click_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = build_info.build_items()
    costs = {}

    for item in items:
        cost = build_info.get_cost(item)
        costs[cost] = item

    cheapest = min(costs)
    if cheapest > cps * time_left:
        return None

    return costs[cheapest]

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    costs = {}

    for item in items:
        cost = build_info.get_cost(item)
        if cost <= cps * time_left + cookies:
            costs[cost] = item

    print costs
    if len(costs) == 0:
        return None
    else:
        most_expensive = max(costs)
        return costs[most_expensive]

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    cps_to_cost_ratio = {}
    max_poss_production = cookies + cps * time_left
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost <= max_poss_production:
            cps = build_info.get_cps(item)
            cps_to_cost_ratio[cps/cost] = item
    if len(cps_to_cost_ratio) > 0:
        return cps_to_cost_ratio[max(cps_to_cost_ratio)]
    return None


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

run()
