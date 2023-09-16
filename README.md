# PortFolioX

Brief description of your project. Explain what it does and why it's useful.

## Features

- **User-Friendly Interface**: Provides a user-friendly web interface for inputting stock tickers, views, and confidences.
- **Portfolio Management**: Allows users to add and remove stocks from their portfolios.
- **Efficient Portfolio Optimization**: Utilizes the PyPortfolioOpt library to optimize portfolios based on user views and confidences.
- **Visualization**: Displays optimized portfolio allocations and allows users to visualize their portfolios.

## Deployment

This project has been deployed using Azure App Service for hosting the web application and Azure Container Registry for containerized deployment.

### Azure App Service

The Stockaroo web application is hosted on Azure App Service, a fully managed platform for building, deploying, and scaling web apps. Azure App Service offers high availability, automatic scaling, and easy integration with Azure services.

### Azure Container Registry

Azure Container Registry is used to store and manage Docker container images for the Stockaroo application. Docker containers make it easy to package the application and its dependencies, ensuring consistency and portability across different environments.

## Getting Started

To get started with Stockaroo, follow these steps:

1. Clone the repository to your local machine.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Run the application using `python app.py`.
4. Access the web interface by opening a web browser and navigating to `http://localhost:5000`.

## Usage

Explain how to use your project. Provide examples and usage scenarios.

1. Start the Flask application: `python app.py`
2. Open a web browser and navigate to `http://localhost:5000` to access the application.
3. Use the web interface to add and remove stocks from your portfolio, specify your views, and set confidences.
4. Click the "Submit" button to optimize your portfolio.



## Technologies Used

List the technologies and libraries/frameworks used in your project.

- Python
- Flask
- HTML/CSS
- yfinance
- NumPy
- Pandas
- PyPortfolioOpt
- Matplotlib

## Screenshots

Include screenshots or images that showcase your project's user interface or functionality.

![Screenshot 1](/screenshots/screenshot1.png)
![Screenshot 2](/screenshots/screenshot2.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
