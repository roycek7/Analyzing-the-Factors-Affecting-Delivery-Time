library(openxlsx)
library(dplyr)
library(stats)
library(ggplot2)
library(tidyr)

olist = consolidated_ecommerce_olist_2
olist_1 = na.omit(olist)
str(olist_1)
NROW(olist_1)

#fix data type
olist_1$hour_of_day = as.factor(olist_1$hour_of_day)


olist_t = distinct(olist_1,olist_1$order_id,.keep_all = T)
olist_t = olist_t %>% group_by(customer_unique_id)
par(mfrow = c(3,1))
plot(olist_t$weekday_purchase)
hist(olist_t$weeknum_purchase)
plot(olist_t$month_purchase)

par(mfrow = c(6,2))

hist(olist_t$price,breaks = 100, xlim = c(0,2000))
olist_t$order_id = as.character(olist_t$order_id)

hist(olist_1$hour_of_day,breaks = 24,xlim = c(0,25))
hist(olist_1$weekday_purchase, breaks = 7)
hist(subset(olist_1$weeknum_purchase,olist_1$year_purchase == 2017))
hist(olist_1$weeknum_purchase)

for (i in 1:12) {
  if (i == 1) {j = "January"}
  else if (i==2){j = "February"}
  else if (i==3){j = "March"}
  else if (i==4){j = "April"}
  else if (i==5){j = "May"}
  else if (i==6){j = "June"}
  else if (i==7){j = "July"}
  else if (i==8){j = "August"}
  else if (i==9){j = "September"}
  else if (i==10){j = "October"}
  else if (i==11){j = "November"}
  else if (i==12){j = "December"}
  else{j==0}
  hist(subset(olist_1$weeknum_purchase,(olist_1$year_purchase == 2017)&(olist_1$month_purchase == i)),main = j, xlab = "Weeknumber of Month",ylab = "Number of Orders", breaks = 5) 
}

for (i in 1:12) {
  if (i == 1) {j = "January"}
  else if (i==2){j = "February"}
  else if (i==3){j = "March"}
  else if (i==4){j = "April"}
  else if (i==5){j = "May"}
  else if (i==6){j = "June"}
  else if (i==7){j = "July"}
  else if (i==8){j = "August"}
  else if (i==9){j = "September"}
  else if (i==10){j = "October"}
  else if (i==11){j = "November"}
  else if (i==12){j = "December"}
  else{j==0}
  hist(subset(olist_1$hour_of_day,(olist_1$year_purchase == 2017)&(olist_1$month_purchase == i)),main = j, xlab = "Hour of Day",ylab = "Number of Orders", breaks = 25) 
}

interaction.plot(olist_1$weeknum_purchase,olist_1$month_purchase,as.integer(olist_1$order_id),col = c(1:12))

par(mfrow = c(2,2))
plot(subset(olist_1$payment_type,(olist_1$year_purchase == 2016)&(!duplicated(olist_1$order_id))),main="2016",xlab='payment type',ylab='number of orders')
plot(subset(olist_1$payment_type,(olist_1$year_purchase == 2017)&(!duplicated(olist_1$order_id))),main="2017",xlab='payment type',ylab='number of orders')
plot(subset(olist_1$payment_type,(olist_1$year_purchase == 2018)&(!duplicated(olist_1$order_id))),main="2018",xlab='payment type',ylab='number of orders')
plot(subset(olist_1$payment_type,(!duplicated(olist_1$order_id))),main="total",xlab='payment type',ylab='number of orders')


str(olist)
