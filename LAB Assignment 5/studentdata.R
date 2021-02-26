#....................ASSIGNMENT 5.......................#

#...................Dependencies.........................

library(bnlearn)
#Do not have name of variable if head is True
subject.marks<-read.table("2020_bn_nb_data.txt",head=TRUE)

#returns first part of table upto 6 rows
head(subject.marks) 

#generates a list of marks in subject columnwise
subject.marks<-lapply(subject.marks,as.factor)
print(subject.marks)

#assign table data into dataframe for further operations
subject.marks<-data.frame(subject.marks)

#Stream creates the plot(structure learning)
#using hill climber which use objective function (score) K2 to find an sub-optimal fit for dataframe among DAG
#Hierarchical clustering based on maximum likelihood criteria for Gaussian mixture models parameterized by eigenvalue decomposition
subject.marks.net<-hc(subject.marks[,-9],score="k2")
plot(subject.marks.net)

#We can use other objective functions or baysien scores like bic or bde which will give different dependency
subject.marks.net<-hc(subject.marks[,-9],score="bic")
plot(subject.marks.net)

subject.marks.net<-hc(subject.marks[,-9],score="bde")
plot(subject.marks.net)


#...................CPT for each subject node...................

subject.marks.net.fit<-bn.fit(subject.marks.net, subject.marks[,-9])
bn.fit.barchart(subject.marks.net.fit$EC100)

subject.marks.net.fit<-bn.fit(subject.marks.net, subject.marks[,-9])
bn.fit.barchart(subject.marks.net.fit$EC160)

subject.marks.net.fit<-bn.fit(subject.marks.net, subject.marks[,-9])
bn.fit.barchart(subject.marks.net.fit$IT101)

subject.marks.net.fit<-bn.fit(subject.marks.net, subject.marks[,-9])
bn.fit.barchart(subject.marks.net.fit$IT161)

subject.marks.net.fit<-bn.fit(subject.marks.net, subject.marks[,-9])
bn.fit.barchart(subject.marks.net.fit$MA101)

subject.marks.net.fit<-bn.fit(subject.marks.net, subject.marks[,-9])
bn.fit.barchart(subject.marks.net.fit$PH100)

subject.marks.net.fit<-bn.fit(subject.marks.net, subject.marks[,-9])
bn.fit.barchart(subject.marks.net.fit$PH160)

subject.marks.net.fit<-bn.fit(subject.marks.net, subject.marks[,-9])
bn.fit.barchart(subject.marks.net.fit$HS101)



#.........Grade Probability for PH100 as per dependencies..........

AA <- cpquery(subject.marks.net.fit, event = (PH100 == "AA"),
               evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD") )

AB <- cpquery(subject.marks.net.fit, event = (PH100 == "AB"),
               evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD") )

BB <- cpquery(subject.marks.net.fit, event = (PH100 == "BB"),
               evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD") )

BC <- cpquery(subject.marks.net.fit, event = (PH100 == "BC"),
               evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD") )

CC <- cpquery(subject.marks.net.fit, event = (PH100 == "CC"),
               evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD") )

CD <- cpquery(subject.marks.net.fit, event = (PH100 == "CD"),
               evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD") )

DD <- cpquery(subject.marks.net.fit, event = (PH100 == "DD"),
               evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD") )

FF <- cpquery(subject.marks.net.fit, event = (PH100 == "F"),
               evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD") )


#..................Naive Bayes Classifier ( Independent ).......................

library(bnclassify)
subject.marks<-read.table("2020_bn_nb_data.txt",head=TRUE)

u <-runif(20)
print(u)
arr = c()
for (i in u)
{
# Splitting data into train and test data
split <- sample.split(subject.marks, SplitRatio = i) 
train_cl <- subset(subject.marks, split == "TRUE") 
test_cl <- subset(subject.marks, split == "FALSE") 

#Creating Dataframe of training and testing data
train_cl<-lapply(train_cl,as.factor)
train_cl<-data.frame(train_cl)
test_cl<-lapply(test_cl,as.factor)
test_cl<-data.frame(test_cl)

#Apply Bayer Classifier on training data 
nb.marks<-nb(class="QP",dataset=train_cl)
plot(nb.marks)

#Prediction using testing data
nb.marks<-lp(nb.marks, test_cl, smooth=0.5)
params(nb.marks)[['QP']]

p<-predict(nb.marks, test_cl)
cm<-table(predicted=p, true=test_cl$QP)

#Accuracy
q<-bnclassify:::accuracy(p, test_cl$QP)
print(q)
arr <- append(arr, q) 

}

print(mean(arr))


#....................Dependent Naive Bayes Classifier...........................

library(bnclassify)
subject.marks<-read.table("2020_bn_nb_data.txt",head=TRUE)

arrq = c()
for (i in u)
{
  # Splitting data into train and test data 
  split <- sample.split(subject.marks, SplitRatio = i) 
  train_cl <- subset(subject.marks, split == "TRUE") 
  test_cl <- subset(subject.marks, split == "FALSE") 
  
  #Creating Dataframe of training and testing data
  train_cl<-lapply(train_cl,as.factor)
  train_cl<-data.frame(train_cl)
  test_cl<-lapply(test_cl,as.factor)
  test_cl<-data.frame(test_cl)
  
  #Apply Bayer Classifier on training data 
  tn <- tan_cl("QP", train_cl)
  tn <- lp(tn, train_cl, smooth = 1)
  plot(tn)
  
  #Prediction using testing data
  nb.marks<-lp(tn, test_cl, smooth=1)
  params(nb.marks)[['QP']]
  
  p<-predict(nb.marks, test_cl)
  cm<-table(predicted=p, true=test_cl$QP)
  
  #Accuracy
  q<-bnclassify:::accuracy(p, test_cl$QP)
  print(q)
  arrq <- append(arrq, q) 

}
print(mean(arrq))







