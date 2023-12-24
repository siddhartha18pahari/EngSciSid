### Interface Functions ###
def initialize():   # Todo: Check if there are globals that aren't defined here!
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it'''

    global cur_time

    global cur_hedons, cur_health

    global last_activity, last_activity_duration

    global tired, last_tired

    global cur_star, cur_star_activity
    global star_counter, star_times, bored_with_stars


    cur_time = 0 # Total elapsed time of simulation (int)

    cur_hedons = 0 # Current hedons points (int)
    cur_health = 0 # Current health points (int)

    last_activity = None # What last activity was (str)
    last_activity_duration = 0 # How long last activity was done (int)

    cur_star = None # What activity was last offered stars (str)
    cur_star_activity = None # What activity is now using stars (str)
    star_counter = 0
    star_times = []
    bored_with_stars = False # True if more than 3 stars in 2h; irreversible after True (bool)

    tired = False # Whether tired (bool)
    last_tired = -1000 # cur_time when tired was last set to True (int)


def perform_activity(activity, duration):   # WIP
    '''The function simulates the user performing activity activity for duration minutes.'''

    global cur_hedons, cur_health, last_activity, last_activity_duration, cur_time, tired, cur_star, last_tired

    remove_tired()  # Checks if tired can be removed, if 120mins passed
    if activity != last_activity:
        last_activity_duration = 0
    cur_time += duration  # Updating after remove_tired check ensures tired not removed by current activity duration >120mins

    # Modify the function calls with the duration
    cur_hedons += estimate_hedons_delta(activity, duration)
    cur_health += estimate_health_delta(activity, duration)

    if star_can_be_taken(activity):  # Adds bonus 3 stars/min for at most 10 mins if star_can_be_taken() == True
        cur_hedons += min(duration, 10) * 3

    cur_star = None  # Clears cur_star after activity, regardless if it was used

    last_activity = activity
    last_activity_duration += duration

    if activity in ["running", "textbooks"]:  # Makes tired if did running or textbooks
        tired = True
        last_tired = cur_time


def get_cur_hedons():
    '''Returns the current amount of hedons as int'''
    return cur_hedons

def get_cur_health():
    '''Returns the current amount of health as int'''
    return cur_health


def offer_star(activity):
    '''Simulates a offering the user a star for engaging in the exercise activity. Assume activity is a string, one of "running", "textbooks", or "resting".'''
    global cur_star, bored_with_stars, star_counter, star_times
    cur_star = activity
    star_counter += 1
    star_times.append(cur_time)

    if star_counter == 3:
        if star_times[-1] - star_times[0] <= 120:
            bored_with_stars = True
            star_counter = 0
            star_times = []


def star_can_be_taken(activity):
    '''Returns True if a star can be used to get more hedons for activity activity. A star can only be taken if no time passed between the star’s being offered and the activity, and the user is not bored with stars, and the star was offered for activity activity.'''
    global bored_with_stars, cur_star
    if bored_with_stars or activity != cur_star:
        return False
    elif activity == cur_star:
        return True


def most_fun_activity_minute(): #WIP
    '''Returns the activity (one of "resting", "running", or "textbooks") which would give the most hedons if the person performed it for one minute at the current time (and circumstances)'''
    #Todo: This is an incredibly janky way to preserve global tired from being changed here
    global tired
    original_tired = tired

    remove_tired()

    activities = ["running", "textbooks", "resting"]
    most_fun_hedons = -100
    most_fun_activity = None
    for activity in activities:
        estimate_hedons = estimate_hedons_delta(activity, 1) + (3 if star_can_be_taken(activity) else 0)
        if estimate_hedons > most_fun_hedons:
            most_fun_hedons = estimate_hedons
            most_fun_activity = activity

    tired = original_tired

    return most_fun_activity


### Helper Functions ###
def remove_tired():
    global tired
    '''Sets tired == False if 120 mins have passed since it was set to True'''
    if cur_time - last_tired > 120:
        tired = False


def get_effective_minutes_left_hedons(activity):
    '''Returns the minutes one could get the larger number of hedons for an activity.'''
    bonus_minutes = {
        "running": 10,
        "textbooks": 20,
        "resting": 0
    }
    return bonus_minutes.get(activity, 0)


def get_effective_minutes_left_health(activity):
    '''Returns the minutes one could get the larger number of health for an activity. Detects if activity has been run previously and subtracts minutes accordingly.'''
    global last_activity, last_activity_duration
    bonus_minutes = {
        "running": 180,
        "textbooks": 0,
        "resting": 0
    }
    if activity == last_activity:
        return max(0, bonus_minutes.get(activity, 0) - last_activity_duration)
    else:
        return bonus_minutes.get(activity, 0)


def estimate_hedons_delta(activity, duration):
    '''Returns the change in hedons if activity is carried out for duration in current circumstances.'''
    global tired

    # resting activity case
    if activity == "resting":
        return 0

    # tired activity case; only computed if not resting
    if tired:
        return -2 * duration

    # running and textbooks activity cases; only computed if not resting or tired
    bonus_time = get_effective_minutes_left_hedons(activity)
    if duration <= bonus_time:
        return duration * (2 if activity == "running" else 1)
    else:
        over_bonus_time = duration - bonus_time
        return bonus_time * (2 if activity == "running" else 1) - over_bonus_time * (2 if activity == "running" else 1)


def estimate_health_delta(activity, duration):
    '''Returns the change in health if activity is carried out for duration in current circumstances.'''
    global last_activity, last_activity_duration
    # resting and textbooks activity cases
    if activity == "resting":
        return 0
    elif activity == "textbooks":
        return duration * 2

    # running activity case; only computed if not resting or textbooks
    bonus_time = get_effective_minutes_left_health(activity)
    if duration <= bonus_time:
        return duration * 3 if activity == "running" else 0
    else:
        over_bonus_time = duration - bonus_time
        return (bonus_time * 3) + (over_bonus_time * 1) if activity == "running" else 0


### Main Block ###
if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons())            # -20 = 10 * 2 + 20 * (-2)             # Test 1
    print(get_cur_health())            # 90 = 30 * 3                          # Test 2
    print(most_fun_activity_minute())  # resting                              # Test 3
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute())  # running                              # Test 4
    perform_activity("textbooks", 30)
    print(get_cur_health())            # 150 = 90 + 30*2                      # Test 5
    print(get_cur_hedons())            # -80 = -20 + 30 * (-2)                # Test 6
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            # 210 = 150 + 20 * 3                   # Test 7
    print(get_cur_hedons())            # -90 = -80 + 10 * (3-2) + 10 * (-2)   # Test 8
    perform_activity("running", 170)
    print(get_cur_health())            # 700 = 210 + 160 * 3 + 10 * 1         # Test 9
    print(get_cur_hedons())            # -430 = -90 + 170 * (-2)              # Test 10

