
**Travel Booking Web Application**

 **Project Overview** 

This is a containerized Travel Booking Web Application that allows users to:
	
  •Register and login
  
	•TO View destinations and travel packages
	
  • Book packages based on date availability
	
  • Make payments
	
  • View booking status
	
  • Admin manage destinations, packages, and bookings

  The project is deployed using Docker and automated through a Jenkins CI/CD pipeline with Blue-Green deployment on AWS.


 **Features**

 **User Features**
 
	• User Registration & Login
  
	• Date-based package booking
	
  • Overlapping date validation
	
  • Dynamic price calculation based on stay duration
	
  • Payment workflow integration
	
  • Booking confirmation page
	
  • Booking cancellation option

 **Admin Features**
	
  • Add / Delete Destinations
	
  • Add / Delete Packages
	
  • Upload images
	
  • View user bookings
	
  • Track payment status
	
  • Monitor availability

 **Booking Logic**

  • Prevents invalid date selection
	
  • Blocks overlapping bookings
	
  • Calculates total price based on number of days
	
  • Tracks available rooms
	
  • Supports cancellation workflow


 **Database Schema**
**Main Tables:**
	
  • users
	
  • destinations
	
  • packages
	
  • bookings
	
  • admins

**Key Concepts:**

  • Foreign key relationship between packages and destinations
	
  • Booking status tracking (PAID / CANCELLED)
	
  • Date-based validation
	
  • Availability management


 **Testing**
**Backend Testing**
	
  • Implemented using Pytest
	
  • Validates booking logic
	
  • Validates overlap detection
	
  • Validates data integrity

**End-to-End Testing**

  • Implemented using Playwright
	
  • Tests:
  
		○ Registration
    
		○ Login
		
    ○ Booking flow
		
    ○ Payment redirection
		
    ○ UI validation

Testing integrated into CI/CD pipeline.


 **Containerization**
	
  • Multi-stage Docker build
	
  • Lightweight Python base image
	
  • Exposed on port 5000
	
  • Image pushed to DockerHub


 **Deployment Architecture**

  • Hosted on AWS EC2
	
  • Application Load Balancer (ALB)
	
  • Blue-Green Deployment using:
	
    ○ Two target groups (Blue & Green)
		
    ○ Traffic switching via ALB
	
  • Zero downtime deployment strategy


 **Monitoring**
	
  • Prometheus for metrics collection
	
  • Grafana for dashboard visualization
	
  • Health check endpoint configured


 **CI/CD Pipeline**
**Implemented using Jenkins:**
	
  1. Code pushed to GitHub
	
  2. Jenkins triggers pipeline
	
  3. Run Pytest
	
  4. Run Playwright tests
	
  5. Build Docker image
	
  6. Push to DockerHub
	
  7. Deploy to EC2 (Blue/Green)


 **Project Structure**

travel_site/

│

├── app.py

├── travel.db

├── requirements.txt

├── Dockerfile

├── Jenkinsfile

│

├── templates/

├── static/

├── tests/

 **How to Run Locally**

 **Clone Repository**

git clone <repo-url>
cd travel_site

 **Create Virtual Environment**

python3 -m venv venv
source venv/bin/activate

 **Install Dependencies**

pip install -r requirements.txt

 **Run Application**

python app.py

Visit:
http://localhost:5000


 **Production Highlights**

  • Zero downtime deployment
	
  • Automated testing pipeline
	
  • Containerized architecture
	
  • Cloud-ready infrastructure
	
  • Blue-Green deployment strategy
	
  • Scalable and monitored environment

