# pyRecommender-tests

## Synopsis
Tests for web application - pyRecommend.

## Application source code
~~~
https://github.com/OrangeKing/pyRecommender
~~~

##Install requirements
~~~
pip install -r requirements.txt
~~~

## Run tests for desktop browser
~~~
behave -D mobile="no" $(cat feature_order.txt)
~~~

## Run tests for mobile browser
~~~
behave -D mobile="default" $(cat feature_order.txt)
~~~

## Run tests for the Iphone 6
~~~
behave -D mobile="iphone" $(cat feature_order.txt)
~~~