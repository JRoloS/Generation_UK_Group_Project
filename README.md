# 🅱🆁🅴🆆🅴🅳 🅰🆆🅰🅺🅴🅽🅸🅽🅶

<p align="center"><img src="Documentation/logo.png" width="175" height="175" /></p>

## Description 


Introducing the Brewed-Awakening Project - an innovative solution that will revolutionize the way Super-Cafe manages its sales data.

As Super-Cafe continues to expand across the country, their sales data has been increasing exponentially, leading to an urgent need for an efficient and effective data management system. The current system of using Comma Separated Values format for tracking data has become outdated and unreliable, leading to a lot of manual work and errors.

With the Brewed-Awakening Project, our team will be creating a state-of-the-art software solution that will meet all of Super-Cafe's data management needs. We aim to deliver a fully functional product by the end of Week 5 that will be ready for testing. Our software will feature core functionality that will help Super-Cafe expertly and efficiently organize its data, leading to improved sales in the long run.

During Week 6, we will focus on refining and polishing the code while adding any new non-essential functions. Our ultimate goal is to provide Super-Cafe with a comprehensive solution that is easy to use and maintain, so they can focus on growing their business domestically and internationally. With our software in place, Super-Cafe will have a competitive edge over its competitors, allowing it to dominate the market and become a leader in the industry.


## Elevator Pitch

**FOR:** SUPER-CAFE COFFEE SHOP<br />
**WHO:** Wants to organise their sales data from multiple branches<br />
**THE:** Brewed Awakening Project<br />
**IS A:** ETL (Export, Transform, Load) Application<br />
**THAT:** Performs and allows Super-Cafe to analyse, organise and take control of their data through pipeline cleansing and visualisation.<br />
**UNLIKE:** Their old system of using CSVs<br />
**OUR PRODUCT:** Will allow them to make sense of their data and spot trends more efficiently as well as solves the problem of data inconsistencies and inaccuracies.<br />

## Built With

The Brewed Awakening project was built using a combination of technologies, including:
* Python 3
* Jupyter Notebook for individual function testing 
* AWS Lambda for severless computing
* PostgreSQL for the local test Database
* CloudWatch Metrics and logs were collected from multiple sources including AWS S3 buckets. 
* Grafana for data visualisation.

## Installation Instructions

This section is a step-by-step guide on how to install and set up the main platforms used for the project.

* Install Python 3 on VS Code. This can be downloaded from the official website [here](https://www.python.org/downloads/) and follow the installation instructions. Once Python 3 is installed, make sure it's added to the system's PATH environment variable.

* Install Docker on your local machine. This can be downloaded from the official website [here](https://www.docker.com//) and follow the installation instructions.

* Set up AWS. We will create an AWS account and set up an S3 bucket to store the project files. Follow the AWS documentation to create an S3 bucket and obtain an access key ID and secret access key.

* Set up Grafana. We'll need to download and install Grafana on our local machine. Once Grafana is installed, open a browser and navigate to http://localhost:3000 to access the Grafana dashboard. Log in with the default username and password (admin/admin).

* Clone the project repository [here](https://github.com/generation-de-lon9/brewed-awakening-final-project). Use Git to clone ```git clone git@github.com:generation-de-lon9/brewed-awakening-final-project.git ``` the project repository to your local machine.

* Install project dependencies by navigating to the project directory and running the following command to install the project dependencies:

```
pip install -r requirements.txt
```
* Change the `docker-compose.yml` variables for `POSTGRES_USER:, POSTGRES_PASSWORD:, POSTGRES_DB:` to your specific choices.
* Set up environment variables. Create a new file named `.env` in the project directory and add the following environment variables:
```
sql_host=localhost
sql_user=[SAME AS IN .YML FILE]
sql_pass=[SAME AS IN .YML FILE]
sql_db=[SAME AS IN .YML FILE]
sql_port=5432
```

```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
GRAFANA_API_KEY=your_grafana_api_key
```
Replace `your_access_key_id`, `your_secret_access_key`, and `your_grafana_api_key` with your actual values.



## Configuration

This section provides information on how to customize the project to meet the specific needs. This section may include details on how to modify settings, configure options, or adjust parameters to optimize the project. By providing clear and concise instructions on how to configure the project, we can help users get the most out of the software and ensure that it meets their unique requirements.


### **Setting up the local Database for testing**

* Choose a database management system (DBMS) e.g. MySQL, PostgreSQL.
* Install the DBMS on your computer. For the Brewed Awakening Project we have chosen to use Adminer SQL for our local testing. [Why?](#why-adminer-sql)
* Time to spin-up the docker container on your local testing machine, first change your directory into the "docker_setup" folder, then run this command:
```
docker compose up -d 
```
* You should then see a docker container ready with two sub containers for the GUI for adminer(8080:8080) and for the internal PostgreSQL database(5432:5432).

* You can then navigate to http://localhost:8080 to log in and interact with your database.


### **Configuring the Database connection**

To configure the database connection using Adminer SQL, you'll need to follow these steps:

* Open your web browser and navigate to the Adminer SQL login page.
* Change the "system" tab from `MYSQL` to `PostgreSQL`. 
* Enter the database server hostname, port number, username, and password (same used in the `docker-compose.yml` and `.env` files).
* Click the "Login" button to log in to the database server.

Once you've logged in to the database server, you should be able to create, edit, and delete databases and tables using the Adminer SQL interface.

* The quickest and easiest way to set-up our exact database schema would involve finding the `import` button in the main select database page. 
* Once on the import page, click `choose files`, navigate to the same directory the local repository is located and find the `BA-Final-Schema.sql` file and upload. 
* Lastly, click `Execute` to create all tables and foreign key constraints instantly, you should end up with the schema below.

### **Database Schema**

<p align="center"><img src="Documentation/schema.png" width="475" height="325" /></p>

### **Customising the Data Schema**

Super-Cafe's data schema can be customized to meet your specific needs. To do this, you'll need to modify the database tables using Adminer SQL. Here's how to add or remove tables and modify the data types of existing fields:



#### **Adding a Table**

To add a new table to the database, follow these steps:

* Log in to the database server using Adminer SQL.
* Click the "SQL command" button to open the SQL command prompt.
* Enter the SQL command to create the new table.
* For example, to create a new table called `orders` with the fields `order_id`, `customer_id`, and `order_date`, you would enter the following SQL command:
   
   ```sql
   CREATE TABLE orders (
     order_id INT PRIMARY KEY,
     customer_id INT,
     order_date DATE
   );
   ```
Here are some other SQL commands to follow

#### **Removing a Table**

```sql
DROP TABLE orders;
```

#### **Adding a One-to-Many Relationship**

To add a one-to-many relationship between two tables in the database, follow these steps:

* Log in to the database server using Adminer SQL.
* Click the "SQL command" button to open the SQL command prompt.
* Enter the SQL command to add a foreign key constraint to the child table.
* For example, to create a one-to-many relationship between the `orders` and `customers` tables using the `customer_id` field, you would enter the following SQL command:
   
   ```sql
   ALTER TABLE orders
   ADD CONSTRAINT fk_orders_customers
   FOREIGN KEY (customer_id)
   REFERENCES customers(customer_id);
   ```
### **AWS Lambda Schema**

The ETL will be contained within one lambda hosted within AWS. A trigger will be set to initiate the lambda whenever a new 'S3 object creation' event occurs, works through the sanitisation/transformation/normalisation stages while values are inserted into the Redshift database. Below is a visual represeantion of the lambda:

<p align="center"><img src="Documentation/Final Lambda Diagram.png" width="600" height="300" /></p>

## ETL Pipeline CloudFormation Setup

This section will walk you through the steps required to set up the ETL pipeline environment in AWS using the provided CloudFormation template in the infra folder. The pipeline assumes that you already have an S3 bucket containing the CSV files that will be processed by the pipeline.

### **Prerequisites**

Before starting, make sure you have the following:
* An AWS account with sufficient permissions to create and manage resources
* The AWS Command Line Interface (CLI) installed and configured on your local machine

### **Step 1: Clone the Repository**

Clone the repository containing the ETL pipeline code to your local machine:

```
git clone <repository_url>
```

Change into the repository directory:

```
cd <repository_directory>
```

### **Step 2: Update Configuration**

Open the CloudFormation YAML file saved in the "infra" folder and update the following parameters:
* BucketNameRawData: Enter the name of the S3 bucket you wish to create or use for the pipeline
* VpcSubnetId: Provide the ID of the Redshift private subnet in your VPC
* SecurityGroupId: Provide the ID of the Redshift security group

Save the changes to the yaml file

### **Step 3: Deploy the CloudFormation Stack**

In your terminal, navigate to the repository directory (if not already there)

Deploy the CloudFormation stack using the AWS CLI:

```
aws cloudformation create-stack --stack-name <stack_name> --template-body file://template.yaml --capabilities CAPABILITY_IAM
```

Replace <stack_name> with a unique name for your CloudFormation stack

Wait for the stack creation to complete. You can monitor the progress in the AWS CloudFormation console or by running the following command:

```
aws cloudformation describe-stacks --stack-name <stack_name> --query "Stacks[0].StackStatus"
```

Once the stack status is CREATE_COMPLETE, the environment has been successfully set up

### **Step 4: Verify Lambda Trigger**

Once the CSV files are uploaded to the S3 bucket, the Lambda function will be triggered automatically for each new file created

You can verify the trigger by checking the AWS Lambda console or by viewing the function's logs

For more information on managing AWS CloudFormation stacks, refer to the [AWS CloudFormation documentation](https://docs.aws.amazon.com/cloudformation/index.html)


### **Executing deployment files**

To deploy changes from your current local branch into AWS you can use the following steps:

```
./deploy_aws_windows.sh <profile-name> # For windows systems

./deploy_aws_unix.sh <profile-name> # For unix systems
```


### **Navigating Directories**

Here are some common commands used to navigate directories in the terminal:

```
"pwd": prints the current working directory
"ls": lists the files and directories in the current working directory
"cd": changes the current working directory to a new directory
"cd ..": changes the current working directory to the parent directory of the current directory
"mkdir": creates a new directory
"rm": removes a file or directory
"cp": copies a file or directory
"mv": moves a file or directory
"touch": creates a new file
```


### **Essential Git Commands**

``` 
`git clone`: Clone a repository from a remote source
`git add`: Add changes to the staging area
`git commit`: Commit changes to the local repository
`git push`: Push changes to a remote repository
`git pull`: Pull changes from a remote repository
`git status`: Show the status of the working directory
`git log`: Show the commit history of the repository
`git branch`: List, create, or delete branches
`git checkout`: Switch branches or restore working tree files
`git merge`: Merge one or more branches into the current branch
`git stash`: Stash changes in a dirty working directory away
```

### **Essential Docker Commands**

```
`docker build`: Build an image from a Dockerfile
`docker run`: Run a container from an image
`docker ps`: List running containers
`docker stop`: Stop a running container
`docker rm`: Remove a container
`docker images`: List images on the local machine
`docker rmi`: Remove an image
`docker logs`: Print the logs of a container
`docker exec`: Run a command inside a running container
`docker-compose up`: Start all the services defined in a docker-compose.yml file
```


## Why Adminer SQL?

There are several benefits to using Adminer SQL as a database management tool:

* Lightweight: Adminer SQL is a lightweight tool that can be easily installed and used on most systems. It has a small memory footprint and can be run on low-resource systems.
* User-friendly interface: Adminer SQL provides a user-friendly web-based interface that makes it easy to manage databases, run queries, and perform other database-related tasks. The interface is intuitive and easy to use, even for users who are not familiar with SQL.
* Multi-database support: Adminer SQL supports several popular database management systems, including MySQL, PostgreSQL, SQLite, and Oracle. This makes it a versatile tool that can be used across a variety of projects and applications.
* Customization: Adminer SQL is highly customizable and can be extended with plugins and themes. This allows users to tailor the tool to their specific needs and preferences.

We preferred to use Adminer SQL for our Brewed Awakening project, over other database management tools for these reasons. Additionally, because it is open source software, it is free to use and can be customized to meet specific needs. Its user-friendly interface and support for multiple database systems make it a popular choice for developers.

## Authors

* [Jorge Rolo](https://github.com/rolojorge)
* [Mohamed Shafie](https://github.com/mashafie)
* [Sadat Awuma](https://github.com/SadCodeBleach) 
* [Saleem Mustafa](https://github.com/sm321000)
* [Shekinah Kimvuidi](https://github.com/shekinah001)


## Acknowledgments

Special Thanks, Inspiration, code snippets, etc.
* [Generation UK Program](https://uk.generation.org/)
* Our Mentors
* [W3 Schools](https://www.w3schools.com/)
* [Trello](https://trello.com/)