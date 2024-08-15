import os
import datetime
from tkinter import *
from tkinter import IntVar
from tkinter import StringVar

# Generate the directory to save the output
home = os.path.expanduser("~")
outDirPath = os.path.join(home, "Projects")
if not os.path.exists(outDirPath):
    os.mkdir(outDirPath)

# Generate the root container for the GUI
root = Tk()
root.title("Observation Worksheet Simulator")
root.geometry("438x916+534+0")

# Initialize the interface mode to entry
interfaceMode = "entry"

# Initialize the timer and interval globals
timeElapsed = 0
currentInterval = 1
editingInterval = 1

# Initialize the interface timer and interval globals
timeElapsedDisp = IntVar(root, 0)
currentIntervalDisp = IntVar(root, 1)
editingIntervalDisp = IntVar(root, 1)
timerState = False

# Initialize the observation data globals
state = {}
state[1] = "Unentered"
general = {}
general[1] = 0
responses = {}
responses[1] = 0
nonResponses = {}
nonResponses[1] = 0
appropriate = {}
appropriate[1] = 0
missed = {}
missed[1] = 0
conversation = {}
conversation[1] = False
comments = {}
comments[1] = ""

# Initialize the interface contained variables
generalDisp = IntVar(root, 0)
responsesDisp = IntVar(root, 0)
nonResponsesDisp = IntVar(root, 0)
appropriateDisp = IntVar(root, 0)
missedDisp = IntVar(root, 0)
commentsDisp = StringVar(root, "")
commentsDisp = StringVar(root, "")

# Initialize the interface wide values
# Buttons with too much text to accommodate this height will use larger values
buttonHt = 2

# Set the title common across screens
title = Label(text="Observation of Peer Engagement")
title.pack(pady=3)


# The observation entry screen
obsF = Frame(root)
obsF.pack(side=TOP, anchor=N, fill=BOTH, expand=1)

# Save the comment in the observation entry interface to the interval data
# Used when going to another screen that will use the interval data
def commentsSave():
    global currentInterval, comments
    comments[currentInterval] = commentsDisp.get()

# CLear color from the state buttons to either allow a new state button to be highlighted or show that no state is active
def clearStateButtons():
    solitaryB.config(fg="black")
    onlookerB.config(fg="black")
    parallelPlayB.config(fg="black")
    parallelAwarenessB.config(fg="black")
    jointEngagementB.config(fg="black")
    gamesWithRulesB.config(fg="black")

# Reset the interval observation entry interface to the defaults
# Used when the timer advances the next the entered interval
def resetDataEntryInterface():
    global currentInterval, state
    
    # Reset the engagement state and conversation buttons
    clearStateButtons()
    conversationB.config(text="Not Enaged in Conversation with Another Child", fg="red")

    # Reset the observation data values
    generalDisp.set(str(0))
    responsesDisp.set(str(0))
    nonResponsesDisp.set(str(0))
    appropriateDisp.set(str(0))
    missedDisp.set(str(0))
    commentsDisp.set("")

# When the timer finishes the minute, increase the interval and add default data for the new interval
def advanceInterval():
    global currentInterval, state, general, responses, nonResponses, appropriate, missed, conversation, comments
    
    # Save the comments from the previous interval
    commentsSave()
    
    # Reset the data entry interface widgets
    resetDataEntryInterface()
    
    # Increment the interval being entered to a new one
    currentInterval += 1
    currentIntervalDisp.set(currentInterval)
    dataLF.config(text="Entering Observation Interval #"+str(currentInterval)+":")
    
    # Fill the data for the new interval with default values
    state[currentInterval] = "Unentered"
    general[currentInterval] = 0
    responses[currentInterval] = 0
    nonResponses[currentInterval] = 0
    appropriate[currentInterval] = 0
    missed[currentInterval] = 0
    conversation[currentInterval] = False
    comments[currentInterval] = ""

# Advance the timer a second if it is running and stop it if it is not
def advanceTimer():
    global timeElapsed, currentInterval
    if timerState:
        if timeElapsed < 59:
            timeElapsed += 1
            timeElapsedDisp.set(timeElapsed)
        else:
            timeElapsed = 0
            timeElapsedDisp.set(0)
            advanceInterval()
        root.after(1000, advanceTimer)

# Toggle the timer button and start the timer if it is started
def toggleTimer():
    global timerState
    if not timerState:
        timerToggleB.config(text=" \n Pause Timer \n ", fg="green")
        timerState = True
        advanceTimer()
    else:
        timerToggleB.config(text=" \n Start Timer \n ", fg="red")
        timerState = False
    root.update()

# The button to go to the previous interval's data
def editPrevInterval():
    global editingInterval
    if editingInterval > 1:
        commentsSave()
        editingInterval -= 1
        updateEditingInterface()

# The button to go to the next interval's data
def editNextInterval():
    global editingInterval, currentInterval
    if editingInterval < currentInterval:
        commentsSave()
        editingInterval += 1
        updateEditingInterface()

# The button to jump to the last interval's data
def editLastInterval():
    global editingInterval, currentInterval
    if editingInterval < currentInterval:
        commentsSave()
        editingInterval = currentInterval
        updateEditingInterface()

# The interface for the timer and interval for the data being entered and edited
intervalLF = LabelFrame(obsF, text="Interval:")
intervalLF.pack(side=TOP, anchor=N, padx=6, ipadx=6, ipady=2, fill=X)

# The editing interval navigation buttons need more than the default height to hold the required text
intervalControlButtonHt = 3

# The interface for monitoring and controling the time and interval for observing and entering data
entryIntervalF = Frame(intervalLF)
entryIntervalF.pack(side=TOP, fill=X, expand=1)
obsIntervalInfoF = Frame(entryIntervalF)
obsIntervalInfoF.pack(side=TOP, padx=3, ipadx=3, fill=X, expand=1)
elapsedTimeLF = LabelFrame(obsIntervalInfoF, text="Time Elapsed(sec):")
elapsedTimeLF.pack(side=LEFT, padx=3, fill=X, expand=1)
elapsedTimeE = Entry(elapsedTimeLF, textvariable=timeElapsedDisp, justify=CENTER, width=6)
elapsedTimeE.pack(side=LEFT, padx=3, pady=3, fill=X, expand=1)
enteringIntervalLF = LabelFrame(obsIntervalInfoF, text="Entering Interval:")
enteringIntervalLF.pack(side=LEFT, padx=3, fill=X, expand=1)
enteringIntervalE = Entry(enteringIntervalLF, textvariable=currentIntervalDisp, justify=CENTER, width=6)
enteringIntervalE.pack(side=LEFT, padx=3, pady=3, fill=X, expand=1)
timerToggleF = Frame(entryIntervalF)
timerToggleF.pack(side=BOTTOM, padx=3, pady=4, ipadx=3, fill=X, expand=1)
timerToggleB = Button(timerToggleF, text=" \n Start Timer \n ", height=intervalControlButtonHt, fg="red", command=toggleTimer)
timerToggleB.pack(side=TOP, fill=X, expand=True)

# Initialize the timer
advanceTimer()

# The container for the editing interval information interface
editIntervalF = Frame(intervalLF)
#editIntervalF.pack(side=TOP, fill=X, expand=1)

# The editing interval index display widgets
editIntervalIndexLF = LabelFrame(editIntervalF, text="Editing Interval:")
editIntervalIndexLF.pack(side=TOP, padx=6, fill=X)
editIntervalIndexE = Entry(editIntervalIndexLF, textvariable=editingIntervalDisp, justify=CENTER, width=6)
editIntervalIndexE.pack(side=TOP, padx=5, pady=3, fill=X)

# The interval navigation buttons
editIntervalNavF = Frame(editIntervalF)
editIntervalNavF.pack(side=BOTTOM, padx=3, pady=4, ipadx=3, fill=X, expand=1)
editIntervalPrevB = Button(editIntervalNavF, text="Previous\nInterval", height=intervalControlButtonHt, command=editPrevInterval)
editIntervalPrevB.pack(side=LEFT, padx=1, fill=X, expand=True)
editIntervalLastB = Button(editIntervalNavF, text="Go to Last\nInterval", height=intervalControlButtonHt, command=editLastInterval)
editIntervalLastB.pack(side=LEFT, padx=1, fill=X, expand=True)
editIntervalNextB = Button(editIntervalNavF, text="Next\nInterval", height=intervalControlButtonHt, command=editNextInterval)
editIntervalNextB.pack(side=LEFT, padx=1, fill=X, expand=True)

def applyEngagementState(interval):
    global state
    
    # Reset the engagement state buttons to defaults
    clearStateButtons()
    
    # Update the interface with the data for the interval being edited
    match state[interval]:
        case "Solitary":
            solitaryB.config(fg="red")
        case "Onlooker":
            onlookerB.config(fg="red")
        case "Parallel Play":
            parallelPlayB.config(fg="red")
        case "Parallel Awareness":
            parallelAwarenessB.config(fg="red")
        case "Joint Engagement":
            jointEngagementB.config(fg="red")
        case "Games with Rules":
            gamesWithRulesB.config(fg="red")
            
# Update the state buttons for the interface mode and active engagement state
def toggleStateButtons(stateName):
    global interfaceMode, currentInterval, editInterval, state
    
    # Set the interval index based on the mode
    if interfaceMode == "entry":
        interval = currentInterval
    else:
        interval = editingInterval
  
    # If button pressed was the previous engagement state, replace the value with the default
    # If button pressed is the new state, display that it is the interval's engagement state
    prevSelection = state[interval]
    if stateName == prevSelection:
        state[interval] = "Unentered"
    else:
        state[currentInterval] = stateName
        
    # Configure the engagement state buttons
    applyEngagementState(interval)

# Fill the data values
def fillDataValues(interval):
    global general, responses, nonResponses, appropriate, missed, comments
    generalDisp.set(general[interval])
    responsesDisp.set(responses[interval])
    nonResponsesDisp.set(nonResponses[interval])
    appropriateDisp.set(appropriate[interval])
    missedDisp.set(missed[interval])
    commentsDisp.set(comments[interval])
    root.update()

# Configure the conversation button
def applyConversation(interval):
    global conversation
    
    # Apply the appropriate conversation button text to the conversation button
    if conversation[interval]:
        conversationB.config(text="Enaged in Conversation with Another Child", fg="green")
    else:
        conversationB.config(text="Not Enaged in Conversation with Another Child", fg="red")
    root.update()

# Toggle the conversation button and data between engaged and not engaged when pressed
def conversationToggle():
    global interfaceMode, conversation

    # Set the interval index based on the mode
    if interfaceMode == "entry":
        interval = currentInterval
    else:
        interval = editingInterval

    # Toggle the conversation value and button label
    conversation[currentInterval] = not conversation[currentInterval]
    applyConversation(interval)
    root.update()

# Configure the data interface to match the data for the interval being manipulated
def fillData(interval):
    applyEngagementState(interval)
    fillDataValues(interval)
    applyConversation(interval)
    root.update()
    
# Update the observation interface with the data for the interval currently being manipulated
def updateEditingInterface():
    global editingInterval
    editingIntervalDisp.set(editingInterval)
    dataLF.config(text="Editing Observation Interval #"+str(editingInterval)+":")
    fillData(editingInterval)
    root.update()

# Interface container for entering observation data
dataLF = LabelFrame(obsF, text="Entering Observation Interval #1:")
dataLF.pack(side=TOP, padx=6, pady=3, ipadx=6, fill=BOTH, expand=True)

# Engagement state buttons for setting the engagement state for the interval
stateLF = LabelFrame(dataLF, text="Engagement State:")
stateLF.pack(side=TOP, padx=6, pady=1, ipadx=6, ipady=3)
stateButtonWidth = 11
stateButtonHt = 3
stateButtonsFirstColumn = Frame(stateLF)
stateButtonsFirstColumn.pack(side=LEFT, padx=1, fill=X, expand=True)
stateButtonsSecondColumn = Frame(stateLF)
stateButtonsSecondColumn.pack(side=LEFT, padx=1, fill=X, expand=True)
stateButtonsThirdColumn = Frame(stateLF)
stateButtonsThirdColumn.pack(side=LEFT, padx=1, fill=X, expand=True)
solitaryB = Button(stateButtonsFirstColumn, text="Solitary", width=stateButtonWidth, height=stateButtonHt,
    command=lambda: toggleStateButtons("Solitary"))
solitaryB.pack(side=TOP, pady=1, fill=X, expand=True)
onlookerB = Button(stateButtonsFirstColumn, text="Onlooker", width=stateButtonWidth, height=stateButtonHt,
    command=lambda: toggleStateButtons("Onlooker"))
onlookerB.pack(side=TOP, pady=1, fill=X, expand=True)
parallelPlayB = Button(stateButtonsSecondColumn, text="Parallel\nPlay", width=stateButtonWidth, height=stateButtonHt,
    command=lambda: toggleStateButtons("Parallel Play"))
parallelPlayB.pack(side=TOP, pady=1, fill=X, expand=True)
parallelAwarenessB = Button(stateButtonsSecondColumn, text="Parallel\nAwareness", width=stateButtonWidth, height=stateButtonHt,
    command=lambda: toggleStateButtons("Parallel Awareness"))
parallelAwarenessB.pack(side=TOP, pady=1, fill=X, expand=True)
jointEngagementB = Button(stateButtonsThirdColumn, text="Joint\nEngagement", width=stateButtonWidth, height=stateButtonHt,
    command=lambda: toggleStateButtons("Joint Engagement"))
jointEngagementB.pack(side=TOP, pady=1, fill=X, expand=True)
gamesWithRulesB = Button(stateButtonsThirdColumn, text="Games\nwith Rules", width=stateButtonWidth, height=stateButtonHt,
    command=lambda: toggleStateButtons("Games with Rules"))
gamesWithRulesB.pack(side=TOP, pady=1, fill=X, expand=True)

# The containers for widgets for entering the number of child initiations
childInitiationsLF = LabelFrame(dataLF, text="Child Initiations:")
childInitiationsLF.pack(side=TOP, padx=6, pady=2, ipadx=6, ipady=3, fill=X)
initiationsButtonWidth = 11
initiationsEntryWidth = 13
generalF = Frame(childInitiationsLF)
generalF.pack(side=LEFT, padx=1, fill=X, expand=True)
responsesF = Frame(childInitiationsLF)
responsesF.pack(side=LEFT, padx=1, fill=X, expand=True)
nonResponsesF = Frame(childInitiationsLF)
nonResponsesF.pack(side=LEFT, padx=1, fill=X, expand=True)

# Increment the interface and data for general initiations
def generalAdd():
    global general
    general[currentInterval] += 1
    generalDisp.set(general[currentInterval])

# Decrement the interface and data for general initiations
def generalSubtract():
    global general
    if general[currentInterval] > 0:
        general[currentInterval] -= 1
        generalDisp.set(general[currentInterval])

# The interface for setting the number of general initiations
generalL = Label(generalF, text="General\nInitiations")
generalL.pack(side=TOP, pady=1, fill=X)
generalAddB = Button(generalF, text="+", width=initiationsButtonWidth, height=buttonHt, command=generalAdd)
generalAddB.pack(side=TOP, pady=1, fill=X)
generalE = Entry(generalF, textvariable=generalDisp, justify=CENTER, width=initiationsEntryWidth)
generalE.pack(side=TOP, pady=1)
generalSubtractB = Button(generalF, text="-", width=initiationsButtonWidth, height=buttonHt, command=generalSubtract)
generalSubtractB.pack(side=TOP, pady=1, fill=X)

# Increment the interface and data for peer responses
def responsesAdd():
    global responses
    responses[currentInterval] += 1
    responsesDisp.set(responses[currentInterval])

# Decrement the interface and data for peer responses
def responsesSubtract():
    global responses
    if responses[currentInterval] > 0:
        responses[currentInterval] -= 1
        responsesDisp.set(responses[currentInterval])

# The interface for setting the number of peer responses
responsesL = Label(responsesF, text="Peer\nResponses")
responsesL.pack(side=TOP, pady=1, fill=X)
responsesAddB = Button(responsesF, text="+", width=initiationsButtonWidth, height=buttonHt, command=responsesAdd)
responsesAddB.pack(side=TOP, pady=1, fill=X)
responsesE = Entry(responsesF, textvariable=responsesDisp, justify=CENTER, width=initiationsEntryWidth)
responsesE.pack(side=TOP, pady=1)
responsesSubtractB = Button(responsesF, text="-", width=initiationsButtonWidth, height=buttonHt, command=responsesSubtract)
responsesSubtractB.pack(side=TOP, pady=1, fill=X)

# Increment the interface and data for peer non-responses
def nonResponsesAdd():
    global nonResponses
    nonResponses[currentInterval] += 1
    nonResponsesDisp.set(nonResponses[currentInterval])

# Decrement the interface and data for peer non-responses
def nonResponsesSubtract():
    global nonResponses
    if nonResponses[currentInterval] > 0:
        nonResponses[currentInterval] -= 1
        nonResponsesDisp.set(nonResponses[currentInterval])

# The interface for setting the number of peer non-responses
nonResponsesL = Label(nonResponsesF, text="Peer\nNon-Responses")
nonResponsesL.pack(side=TOP, pady=1, fill=X)
nonResponsesAddB = Button(nonResponsesF, text="+", width=initiationsButtonWidth, height=buttonHt, command=nonResponsesAdd)
nonResponsesAddB.pack(side=TOP, pady=1, fill=X)
nonResponsesE = Entry(nonResponsesF, textvariable=nonResponsesDisp, justify=CENTER, width=initiationsEntryWidth)
nonResponsesE.pack(side=TOP, pady=1)
nonResponsesSubtractB = Button(nonResponsesF, text="-", width=initiationsButtonWidth, height=buttonHt, command=nonResponsesSubtract)
nonResponsesSubtractB.pack(side=TOP, pady=1, fill=X)

# The containers for widgets for entering the number of child responses
childResponses = LabelFrame(dataLF, text="Child Responses:")
childResponses.pack(side=TOP, padx=6, pady=2, ipadx=6, ipady=3, fill=X)
responsesButtonWidth = 11
responsesEntryWidth = 21
appropriateF = Frame(childResponses)
appropriateF.pack(side=LEFT, padx=1, fill=X, expand=True)
missedF = Frame(childResponses)
missedF.pack(side=LEFT, padx=1, fill=X, expand=True)

# Increment the interface and data for appropriate responses
def appropriateAdd():
    global appropriate
    appropriate[currentInterval] += 1
    appropriateDisp.set(appropriate[currentInterval])

# Decrement the interface and data for appropriate responses
def appropriateSubtract():
    global appropriate
    if appropriate[currentInterval] > 0:
        appropriate[currentInterval] -= 1
        appropriateDisp.set(appropriate[currentInterval])

# The interface for setting the number of appropriate responses
appropriateL = Label(appropriateF, text="Appropriate Responses")
appropriateL.pack(side=TOP, pady=1, fill=X)
appropriateAddB = Button(appropriateF, text="+", width=responsesButtonWidth, height=buttonHt, command=appropriateAdd)
appropriateAddB.pack(side=TOP, pady=1, fill=X)
appropriateE = Entry(appropriateF, textvariable=appropriateDisp, justify=CENTER, width=responsesEntryWidth)
appropriateE.pack(side=TOP, pady=1)
appropriateSubtractB = Button(appropriateF, text="-", width=responsesButtonWidth, height=buttonHt, command=appropriateSubtract)
appropriateSubtractB.pack(side=TOP, pady=1, fill=X)

# Increment the interface and data for missed opportunities
def missedAdd():
    global missed
    missed[currentInterval] += 1
    missedDisp.set(missed[currentInterval])

# Decrement the interface and data for missed opportunities
def missedSubtract():
    global missed
    if missed[currentInterval] > 0:
        missed[currentInterval] -= 1
        missedDisp.set(missed[currentInterval])

# The interface for setting the number of missed opportunities
missedL = Label(missedF, text="Missed Opportunities")
missedL.pack(side=TOP, pady=1, fill=X)
missedAddB = Button(missedF, text="+", width=responsesButtonWidth, height=buttonHt, command=missedAdd)
missedAddB.pack(side=TOP, pady=1, fill=X)
missedE = Entry(missedF, textvariable=missedDisp, justify=CENTER, width=responsesEntryWidth)
missedE.pack(side=TOP, pady=1)
missedSubtractB = Button(missedF, text="-", width=responsesButtonWidth, height=buttonHt, command=missedSubtract)
missedSubtractB.pack(side=TOP, pady=1, fill=X)

# The button to hold the conversation state and switch it when pressed
conversationB = Button(dataLF, text="Not Enaged in Conversation with Another Child", fg="red", height=buttonHt, command=conversationToggle)
conversationB.pack(side=TOP, padx=4, pady=4, fill=X)

# The entry for any comments about the interval being entered
commentsLF = LabelFrame(dataLF, text="Comments:")
commentsLF.pack(side=TOP, padx=6, fill=X)
commentsE = Entry(commentsLF, textvariable=commentsDisp, width=45)
commentsE.pack(side=TOP, padx=4, pady=6, fill=X)

# Container for the summary and save screen
summaryF = Frame(root)
summaryF.pack(side=TOP, fill=BOTH, expand=1)

# Container for ratings interface
ratingLF = LabelFrame(summaryF, text="Child Behavior Rating:")
ratingLF.pack(side=TOP, padx=6, pady=3, ipadx=6, ipady=3, fill=X)

# Set defaults for BEHAM data
behamInitiated = 0
behamResponded = 0
behamConversation = 0
behamGame = 0
beham = 0

# Set defaults for interface displayed BEHAM data
behamInitiatedDisp = IntVar(root, 0)
behamRespondedDisp = IntVar(root, 0)
behamConversationDisp = IntVar(root, 0)
behamGameDisp = IntVar(root, 0)
behamDisp = IntVar(root, 0)

# Interface for displaying the BEHAM
amountLF = LabelFrame(ratingLF, text="Amount:")
amountLF.pack(side=TOP, padx=6, pady=3, ipadx=6, ipady=3, fill=X)
skillsF = Frame(amountLF)
skillsF.pack(side=TOP, padx=6, pady=6, fill=X)
initiatedF = Frame(skillsF)
initiatedF.pack(side=TOP, fill=X)
respondedF = Frame(skillsF)
respondedF.pack(side=TOP, fill=X)
conversationF = Frame(skillsF)
conversationF.pack(side=TOP, fill=X)
gameF = Frame(skillsF)
gameF.pack(side=TOP, fill=X)
initiatedE = Entry(initiatedF, textvariable=behamInitiatedDisp, width=3, justify=CENTER)
initiatedE.pack(side=LEFT)
initiatedL = Label(initiatedF, text=" Initiated to another Child")
initiatedL.pack(side=LEFT)
respondedE = Entry(respondedF, textvariable=behamRespondedDisp, width=3, justify=CENTER)
respondedE.pack(side=LEFT)
respondedL = Label(respondedF, text=" Responded to another Child")
respondedL.pack(side=LEFT)
conversationE = Entry(conversationF, textvariable=behamConversationDisp, width=3, justify=CENTER)
conversationE.pack(side=LEFT)
conversationL = Label(conversationF, text=" Engaged in a Conversation with another Child")
conversationL.pack(side=LEFT)
gameE = Entry(gameF, textvariable=behamGameDisp, width=3, justify=CENTER)
gameE.pack(side=LEFT)
gameL = Label(gameF, text=" Engaged in Game w/ another Child or Group")
gameL.pack(side=LEFT)
behamF = Frame(amountLF)
behamF.pack(side=TOP, padx=6, fill=X)
behamL = Label(behamF, text="Amount Rating (BEHAM):")
behamL.pack(side=LEFT)
behamE = Entry(behamF, textvariable=behamDisp, width=3, justify=CENTER)
behamE.pack(side=LEFT)

# Initialize the BEHQ
behq = 0

# Interface for setting the BEHQ
behqLF = LabelFrame(ratingLF, text="Quality Rating (BEHQ):")
behqLF.pack(side=TOP, padx=6, pady=3, ipadx=6, ipady=3)
behqL = Label(behqLF, text="The execution ability of observed skills", justify=LEFT)
behqL.pack(side=TOP, anchor=NW, padx=6, pady=3)
behqButtonWidth = 11
behqButtonHt = 3
behqButtonsF = Frame(behqLF)
behqButtonsF.pack(side=TOP, padx=2)
behqButtonsFirstF = Frame(behqButtonsF)
behqButtonsFirstF.pack(side=TOP, padx=1, fill=X)
behqButtonsSecondF = Frame(behqButtonsF)
behqButtonsSecondF.pack(side=TOP, padx=1, fill=X)
behqOneB = Button(behqButtonsFirstF, text="1. Poor\nimplementation", width=behqButtonWidth, height=behqButtonHt, command=lambda: updateBEHQButtons(1))
behqOneB.pack(side=LEFT, anchor=W, padx=2, pady=1)
behqTwoB = Button(behqButtonsFirstF, text="2. Less than\nAdequate", width=behqButtonWidth, height=behqButtonHt, command=lambda: updateBEHQButtons(2))
behqTwoB.pack(side=LEFT, anchor=W, padx=2, pady=1)
behqThreeB = Button(behqButtonsFirstF, text="3. Adequate,\noccasional\ndifficulty", width=behqButtonWidth, height=behqButtonHt,
    command=lambda: updateBEHQButtons(3))
behqThreeB.pack(side=LEFT, anchor=W, padx=2, pady=1)
behqFourB = Button(behqButtonsSecondF, text="4. Good,\na couple of\nsmall errors", width=behqButtonWidth, height=behqButtonHt,
    command=lambda: updateBEHQButtons(4))
behqFourB.pack(side=LEFT, anchor=W, padx=2, pady=1)
behqFiveB = Button(behqButtonsSecondF, text="5. Excellent,\nflawless\nimplementation", width=behqButtonWidth, height=behqButtonHt,
    command=lambda: updateBEHQButtons(5))
behqFiveB.pack(side=LEFT, anchor=W, padx=2, pady=1)

# Manage the button states and setting the value for the BEHQ
def updateBEHQButtons(updateBEHQ):
    global behq
    behqOneB.config(fg="black")
    behqTwoB.config(fg="black")
    behqThreeB.config(fg="black")
    behqFourB.config(fg="black")
    behqFiveB.config(fg="black")
    if updateBEHQ == behq:
        behq = 0
    else:
        behq = updateBEHQ
        match behq:
            case 1:
                behqOneB.config(fg="red")
            case 2:
                behqTwoB.config(fg="red")
            case 3:
                behqThreeB.config(fg="red")
            case 4:
                behqFourB.config(fg="red")
            case 5:
                behqFiveB.config(fg="red")
    root.update()

# Initialize the RESDA
resda = 0

# Interface for setting the RESDA
resdaLF = LabelFrame(ratingLF, text="Developmental Appropriateness Rating (RESDA):")
resdaLF.pack(side=TOP, padx=6, pady=3, ipadx=6, ipady=3)
resdaL = Label(resdaLF, text="Accuracy of matching strategies used to child’s\ndevelopmental level in terms of amount and frequency", justify=LEFT)
resdaL.pack(side=TOP, anchor=NW, padx=6, pady=3)
resdaButtonWidth = 11
resdaButtonHt = 3
resdaButtonsF = Frame(resdaLF)
resdaButtonsF.pack(side=TOP, padx=2)
resdaButtonsFirstF = Frame(resdaButtonsF)
resdaButtonsFirstF.pack(side=TOP, padx=1, fill=X)
resdaButtonsSecondF = Frame(resdaButtonsF)
resdaButtonsSecondF.pack(side=TOP, padx=1, fill=X)
resdaOneB = Button(resdaButtonsFirstF, text="1. Poor", width=resdaButtonWidth, height=resdaButtonHt, command=lambda: updateRESDAButtons(1))
resdaOneB.pack(side=LEFT, anchor=W, padx=2, pady=1)
resdaTwoB = Button(resdaButtonsFirstF, text="2. Isolated", width=resdaButtonWidth, height=resdaButtonHt, command=lambda: updateRESDAButtons(2))
resdaTwoB.pack(side=LEFT, anchor=W, padx=2, pady=1)
resdaThreeB = Button(resdaButtonsFirstF, text="3. Average", width=resdaButtonWidth, height=resdaButtonHt, command=lambda: updateRESDAButtons(3))
resdaThreeB.pack(side=LEFT, anchor=W, padx=2, pady=1)
resdaFourB = Button(resdaButtonsSecondF, text="4. Good", width=resdaButtonWidth, height=resdaButtonHt, command=lambda: updateRESDAButtons(4))
resdaFourB.pack(side=LEFT, anchor=W, padx=2, pady=1)
resdaFiveB = Button(resdaButtonsSecondF, text="5. Excellent", width=resdaButtonWidth, height=resdaButtonHt, command=lambda: updateRESDAButtons(5))
resdaFiveB.pack(side=LEFT, anchor=W, padx=2, pady=1)

# Manage the button states and setting the value for the RESDA
def updateRESDAButtons(updateRESDA):
    global resda
    resdaOneB.config(fg="black")
    resdaTwoB.config(fg="black")
    resdaThreeB.config(fg="black")
    resdaFourB.config(fg="black")
    resdaFiveB.config(fg="black")
    if updateRESDA == resda:
        resda = 0
    else:
        resda = updateRESDA
        match resda:
            case 1:
                resdaOneB.config(fg="red")
            case 2:
                resdaTwoB.config(fg="red")
            case 3:
                resdaThreeB.config(fg="red")
            case 4:
                resdaFourB.config(fg="red")
            case 5:
                resdaFiveB.config(fg="red")
    root.update()

# Set the defaults for the information about the session
nameDisp = StringVar(root, "")
locationDisp = StringVar(root, "")
dateDisp = StringVar(root, "")
timeDisp = StringVar(root, "")
timePntDisp = StringVar(root, "Observation Session 1")
observerDisp = StringVar(root, "")

# Interface for information about the observation session
nameF = Frame(summaryF)
nameF.pack(side=TOP, anchor=W, padx=6, pady=3, fill=X)
locationF = Frame(summaryF)
locationF.pack(side=TOP, anchor=W, padx=6, pady=3, fill=X)
dateF = Frame(summaryF)
dateF.pack(side=TOP, anchor=W, padx=6, pady=3, fill=X)
timeF = Frame(summaryF)
timeF.pack(side=TOP, anchor=W, padx=6, pady=3, fill=X)
timePntF = Frame(summaryF)
timePntF.pack(side=TOP, anchor=W, padx=6, pady=3, fill=X)
observerF = Frame(summaryF)
observerF.pack(side=TOP, anchor=W, padx=6, pady=3, fill=X)
nameL = Label(nameF, text="Name:", justify=LEFT)
nameL.pack(side=LEFT, anchor=W)
nameE = Entry(nameF, textvariable=nameDisp, width=38)
nameE.pack(side=RIGHT, anchor=E)
locationL = Label(locationF, text="Location:", justify=LEFT)
locationL.pack(side=LEFT, anchor=W)
locationE = Entry(locationF, textvariable=locationDisp, width=38)
locationE.pack(side=RIGHT, anchor=E)
dateL = Label(dateF, text="Date:", justify=LEFT)
dateL.pack(side=LEFT, anchor=W)
dateE = Entry(dateF, textvariable=dateDisp, width=38)
dateE.pack(side=RIGHT, anchor=E)
timeL = Label(timeF, text="Time:", justify=LEFT)
timeL.pack(side=LEFT, anchor=W)
timeE = Entry(timeF, textvariable=timeDisp, width=38)
timeE.pack(side=RIGHT, anchor=E)
timePntL = Label(timePntF, text="Time Point:", justify=LEFT)
timePntL.pack(side=LEFT, anchor=W)
timePntE = Entry(timePntF, textvariable=timePntDisp, width=38)
timePntE.pack(side=RIGHT, anchor=E)
observerL = Label(observerF, text="Observer:", justify=LEFT)
observerL.pack(side=LEFT, anchor=W)
observerE = Entry(observerF, textvariable=observerDisp, width=38)
observerE.pack(side=RIGHT, anchor=E)

# Withdraw the summary screen to use the observation screen at start
summaryF.pack_forget()

# Clear the foot frame so that the buttons can be packed again neatly
def clearFootButtons():
    obsB.pack_forget()
    editingB.pack_forget()
    summaryB.pack_forget()
    saveB.pack_forget()

# Go back to the observation entry screen with the edited data
def goToObservation():
    global interfaceMode, currentInterval
    
    # Save the last edited comments to the data
    commentsSave()
    
    # Bring up the observation entry screen
    summaryF.pack_forget()
    obsF.pack(side=TOP, fill=BOTH, expand=1)
    interfaceMode = "entry"
    dataLF.config(text="Entering Observation Interval #"+str(currentInterval)+":")
    
    # Switch the interval interface to entry
    editIntervalF.pack_forget()
    entryIntervalF.pack(side=TOP, fill=X, expand=1)

    # Fill the interface with the values for the last observation interval being entered
    fillData(currentInterval)
    
    # Configure the foot buttons
    clearFootButtons()
    summaryB.pack(side=RIGHT)
    editingB.pack(side=RIGHT)

    # Update the app
    root.update()

# Switch to the editing screen
def goToEditing():
    global timerState, editingInterval
    
    # Save any comments entered for the last interval
    commentsSave()
    
    # Switch from the summary screen to the observation screen
    summaryF.pack_forget()
    obsF.pack(side=TOP, fill=BOTH, expand=1)
    interfaceMode = "editing"

    # Because data collection from observation has stopped, pause the timer
    timerToggleB.config(text=" \n Start Timer \n ", fg="red")
    timerState = False
    
    # Switch the interval interface to editing
    entryIntervalF.pack_forget()
    editIntervalF.pack(side=TOP, fill=X, expand=1)
    
    # Configure the interface with the data for the interval being edited
    updateEditingInterface()
    
    # Configure the foot buttons
    clearFootButtons()
    obsB.pack(side=LEFT)
    summaryB.pack(side=RIGHT)

    # Update the interface
    root.update()

# Go to summary and save screen
def goToSummary():
    global currentInterval, state, general, responses, nonResponses, appropriate, missed, conversation
    global behamInitiatedDisp, behamRespondedDisp, behamConversationDisp, behamGameDisp, behamDisp, timeDisp
    
    # Save the last edited comments so that they can be saved
    commentsSave()
    
    # Bring up the summary and save screen
    obsF.pack_forget()
    summaryF.pack(side=TOP, fill=BOTH, expand=1)
    interfaceMode = "summary"

    # Configure the foot buttons
    clearFootButtons()
    obsB.pack(side=LEFT)
    editingB.pack(side=LEFT)
    saveB.pack(side=RIGHT)

    # Generate the BEHAM values to fill in the summary data
    for i in range(1, currentInterval):
        if general[i] > 0:
            behamInitiatedDisp.set(str(1))
        if responses[i] > 0:
            behamInitiatedDisp.set(str(1))
        if nonResponses[i] > 0:
            behamInitiatedDisp.set(str(1))
        if appropriate[i] > 0:
            behamRespondedDisp.set(str(1))
        if missed[i] > 0:
            behamRespondedDisp.set(str(1))
        if conversation[i]:
            behamConversationDisp.set(str(1))
        if state[i] == "Games with Rules":
            behamGameDisp.set(str(1))
    behamDisp.set(str(behamInitiatedDisp.get() + behamRespondedDisp.get() + behamConversationDisp.get() + behamGameDisp.get()))
    
    # Generate the defaults for the observation session information
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    dateDisp.set(str(month) + "/" + str(day) + "/" + str(year))
    hour = now.hour
    minute = now.minute
    half = "AM"
    if hour > 11:
        half = "PM"
        if hour > 12:
            hour -= 12
    elif hour == 0:
        hour = 12
    timeDisp.set(str(hour) + ":" + str(minute) + half)
    
    # Force Tkinter to draw the entry contents, because its buggy
    nameE.focus()
    
# Save all of the observation data to be used outside of the app
def save():
    global outDirPath, currentInterval, state, general, responses, nonResponses, appropriate, missed, conversation, comments, behq, resda
    
    # Set the file to save the observation data for the intervals
    filePath = os.path.join(outDirPath, "Observation Worksheet Observations.tsv")
    filePtr = open(filePath, "w")
    
    # Write the column labels
    h1 = "Interval\tState\tChild Initiations\t\t\tChild Responses\t\tConversation\tComments (note affect, activity, atypical behavior, who the child engages with (aide, adult, peers) and anything of importance or interest)"
    filePtr.write(h1 + "\n")
    h2 = "\t\tGeneral Initiation\tPeer Responses\tPeer Non-Responses\tAppropriate Responses\tMissed Opportunities\t"
    filePtr.write(h2 + "\n")
    
    # Write the observation data by row for each interval
    for i in range(1, currentInterval + 1):
        s = state[i]
        g = str(general[i])
        r = str(responses[i])
        nR = str(nonResponses[i])
        a = str(appropriate[i])
        m = str(missed[i])
        if conversation[i]:
            cn = "Engaged"
        else:
            cn = "Not Engaged"
        cm = comments[i]
        l = str(i) + "\t" + s + "\t" + g + "\t" + r + "\t" + nR + "\t" + a + "\t" + m + "\t" + cn + "\t" + cm
        filePtr.write(l + "\n")

    # Save the obervations by interval data file
    filePtr.close()
    
    # Set the file to save the summary data for the subject
    filePath = os.path.join(outDirPath, "Observation Worksheet Summary.tsv")
    filePtr = open(filePath, "w")
  
    # Write the header for the ratings
    filePtr.write("Child Behavior Rating\n")
    
    # Write the header for the BEHAM
    filePtr.write("\tAmount:\n")

    # Write for each skill whether it was demonstrated
    v = behamInitiatedDisp.get()
    l = "\t\t" + str(v) + "\tInitiated to another Child"
    filePtr.write(l + "\n")
    v = behamRespondedDisp.get()
    l = "\t\t" + str(v) + "\tResponded to another Child"
    filePtr.write(l + "\n")
    v = behamConversationDisp.get()
    l = "\t\t" + str(v) + "\tEngaged in a Conversation (4+ exchanges) with another Child"
    filePtr.write(l + "\n")
    v = behamGameDisp.get()
    l = "\t\t" + str(v) + "\tEngaged in a Game with another Child or Group of Children"
    filePtr.write(l + "\n")
    
    # Write the total of the skills for the BEHAM
    v = behamDisp.get()
    l = "\t\t\tAmount Rating (BEHAM):\t" + str(v) + "\t(Sum the number of skills above)"
    filePtr.write(l + "\n")
    filePtr.write("\n")

    # Write the BEHQ
    match behq:
        case 0:
            ending = "Unentered\t"
        case 1:
            ending = "1\tPoor implementation"
        case 2:
            ending = "2\tLess than Adequate"
        case 3:
            ending = "3\tAdequate, occasional difficulty"
        case 4:
            ending = "4\tGood, a couple of small errors"
        case 5:
            ending = "5\tExcellent, flawless implementation"
    filePtr.write("\t\t\tQuality Rating (BEHQ):\t" + ending + "\n")
    
    # Write the RESDA
    match resda:
        case 0:
            mid = "Unentered\t"
        case 1:
            mid = "1\tPoor"
        case 2:
            mid = "2\tIsolated"
        case 3:
            mid = "3\tAverage"
        case 4:
            mid = "4\tGood"
        case 5:
            mid = "5\tExcellent"
    beginning = "\t\t\tDevelopmental Appropriateness Rating (RESDA):\t"
    ending = " matching of amount and frequency of strategies used."
    l = beginning + mid + ending
    filePtr.write(l + "\n")

    # Write the information about the obervation session
    filePtr.write("\n")
    filePtr.write("Name:\t" + nameDisp.get() + "\n")
    filePtr.write("Location:\t" + locationDisp.get() + "\n")
    filePtr.write("Date:\t" + dateDisp.get() + "\n")
    filePtr.write("Time:\t" + timeDisp.get() + "\n")
    filePtr.write("Time Point:\t" + timePntDisp.get() + "\n")
    filePtr.write("Observer:\t" + observerDisp.get() + "\n")
    
    # Save the summary file
    filePtr.close()

# The container for foots buttons for switching between entering and editing and also saving the data
footF = Frame(root)
footF.pack(side=BOTTOM, padx=6, ipadx=6, ipady=3, fill=X)

# Buttons to go to other screens and to save
footButtonWidth = 12
obsB = Button(footF, text="Go to\nObservation", width=footButtonWidth, height=3, command=goToObservation)
editingB = Button(footF, text="Go to\nEditing", width=footButtonWidth, height=3, command=goToEditing)
summaryB = Button(footF, text="Go to\nSummary", width=footButtonWidth, height=3, command=goToSummary)
saveB = Button(footF, text="Save", width=footButtonWidth, height=3, command=save)
summaryB.pack(side=RIGHT)
editingB.pack(side=RIGHT)

# Start the app
root.mainloop()
