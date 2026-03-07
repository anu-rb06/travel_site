**Travel Booking Web Application**

 **Project Overview**

This is a containerized Travel Booking Web Application designed with production-ready DevOps practices.

The system enables users to browse destinations, book travel packages, and complete payments while ensuring availability validation and booking consistency.

The application is deployed on AWS using:
	
	• Docker containerization
	
	• Jenkins CI/CD automation
	
	• Blue-Green deployment strategy

	• Application Load Balancer (ALB)

	• Prometheus & Grafana monitoring


🧩 **Architecture Overview**

Developer → GitHub → Jenkins CI/CD → DockerHub → AWS EC2 (Blue/Green) → ALB → End Users


**Deployment Flow**
	
	1. Code pushed to GitHub
	
	2. Jenkins pipeline triggered
	
	3. Automated testing (Pytest & Playwright)
	
	4. Docker image built & pushed to DockerHub
	
	5. Deployment to inactive environment (Blue/Green)
	
	6. ALB switches traffic

	7. Zero downtime release


🛠 **Tech Stack**

Backend: Python (Flask)

Database: SQLite

Testing: Pytest, Playwright

CI/CD: Jenkins

Containerization: Docker

Cloud Infrastructure: AWS EC2, ALB

Monitoring: Prometheus, Grafana

Version Control: Git & GitHub

🚀 **Application Features**

👤 **User Features**
	
	• User Registration & Login
	
	• Browse destinations & packages
	
	• Date-based package booking
	
	• Overlapping date validation
	
	• Dynamic price calculation
	
	• Integrated payment workflow
	
	• Booking confirmation page

	• Booking cancellation option


🛠 **Admin Features**
	
	• Add / Delete Destinations
	
	• Add / Delete Packages
	
	• Image uploads
	
	• View all user bookings
	
	• Track payment status

	• Monitor room availability


📅 **Booking Logic**
	
	• Prevents invalid date selection
	
	• Blocks overlapping bookings

	• Calculates total cost based on stay duration

	• Tracks available rooms dynamically

	• Supports cancellation workflow

🗄 **Database Schema**

**Main Tables**
	
	• users
	
	• destinations
	
	• packages
	
	• bookings
	
	• admins

**Design Concepts**
	
	• Foreign key relationship between packages and destinations
	
	• Booking status tracking (PAID / CANCELLED)
	
	• Date validation logic
	
	• Availability management system

🧪 Testing Strategy

**Backend Testing (Pytest)**
	
	• Booking validation
	
	• Overlap detection
	
	• Data integrity checks
	
	• Business logic verification

**End-to-End Testing (Playwright)**
	
	• Registration flow
	
	• Login flow
	
	• Booking process
	
	• Payment redirection
	
	• UI validation

All tests are integrated into the CI/CD pipeline.

🐳 **Containerization**
	
	• Multi-stage Docker build
	
	• Lightweight Python base image
	
	• Exposed on port 5000
	
	• Image pushed to DockerHub
	
	• Environment-ready container

☁ **Cloud Deployment Architecture**

	• Hosted on AWS EC2
	
	• Application Load Balancer (ALB)
	
	• Blue-Green Deployment Strategy
	
	• Two target groups (Blue & Green)
	
	• Traffic switching through ALB
	
	• Zero downtime releases

🔁 **Blue-Green Deployment Strategy**
	
	• Two identical environments: Blue & Green
	
	• One environment actively serves traffic
	
	• New version deployed to inactive environment
	
	• After validation, ALB switches traffic
	
	• Ensures zero downtime and safe rollback

📊 **Monitoring & Observability**
	
	• Prometheus for metrics collection
	
	• Grafana dashboards for visualization
	
	• Health-check endpoint configured
	
	• Application uptime monitoring

🔐 **Security Implementation**
	
	• SSH key-based authentication
	
	• AWS Security Group configuration
	
	• Admin role-based access
	
	• Input validation to prevent invalid bookings

📈 **Scalability**
	
	• Container-based architecture enables scaling
	
	• ALB supports multiple EC2 instances
	
	• Monitoring ensures performance tracking
	
	• Blue-Green ensures safe release cycles

🔄 **CI/CD Pipeline (Jenkins)**

**Pipeline Stages:**
	
	1. Code checkout from GitHub
	
	2. Run Pytest
	
	3. Run Playwright E2E tests
	
	4. Build Docker image
	
	5. Push image to DockerHub
	
	6. Deploy to AWS EC2 (Blue/Green)
	
	7. Switch traffic via ALB

📁 **Project Structure**

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

⚙️ **Run Locally**

1️⃣ **Clone Repository**

git clone <repo-url>

cd travel_site

2️⃣ **Create Virtual Environment**

python3 -m venv venv

source venv/bin/activate

3️⃣ **Install Dependencies**

pip install -r requirements.txt

4️⃣ **Run Application**

python app.py

**Visit:**

http://localhost:5000

