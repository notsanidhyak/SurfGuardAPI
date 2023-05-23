# SurfGuardAPI
<br>

> Yes, of course we all are athletics. We surf the internet everyday!
<br>

SurfGuardAPI is the brain behind [SurfGuard](https://github.com/notsanidhyak/SurfGuard-Chrome), a plugin for browsers which helps you surf the internet waves safely and securely. It thoroughly analyzes the site you are on and tells you whether it is safe to surf or not. The analysis is done by this custom made SurfGuard API which uses ML model having over 92.79% accuracy on training data and 92.67% accuracy on testing data.
<br>
<br>

### ⚡ How to use API?
<br>

- The API is live [here](https://surfguardsays.onrender.com) and can handle upto **maximum 8** concurrent requests.

- Send a GET request to 
```
https://surfguardsays.onrender.com/getStatus?url=<url_you_wish_to_analyze>
```

- Response is sent within 10-15 seconds but may take up to 25 seconds in few scenarios.
<br>

### 🤝 How to Contibute?
<br>

- Take a look at the Existing [Issues](https://github.com/notsanidhyak/SurfGuardAPI/issues) or create your own Issues!
- Wait for the Issue to be assigned to you.
- Fork the repository
- Clone your forked copy of the project.
<br>

```
git clone --depth 1 https://github.com/<your_user_name>/SurfGuardAPI.git
```
<br>

### 💻 Installation
<br>

1. [Download](https://www.python.org/) and setup python on your device
2. Install dependencies

```
pip install -r requirements.txt
```
3. Run start command

```
gunicorn main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
```

<br>

### ❤️ Feedback
<br>

If you have any feedback or suggestions please reach out to the project admin [sanidhyak](https://github.com/notsanidhyak) or you can create a [issue](https://github.com/notsanidhyak/SurfGuardAPI/issues) and mention there which new features can be added to make SurfGuard better.

