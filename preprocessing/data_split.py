from sklearn.model_selection import train_test_split

###Implementation for splitting the data###
#splits data and expected results based on percentage of data that will be for testing
def splitData(data, results, percentTest):
    inputTraining, inputTest, resultTraining, resultTest = train_test_split(data, results, test_size=percentTest, stratify = results)
    return (inputTraining, inputTest, resultTraining, resultTest)