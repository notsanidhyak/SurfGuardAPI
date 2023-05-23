![SurfGuardAPI_Banner](https://github.com/notsanidhyak/SurfGuardAPI/assets/86651116/f57ba747-a1c8-4576-8071-5300735fc1f2)


# SURFGUARDAPI
<br>

> Yes, of course we all are athletics. We surf the internet everyday!
<br>

SURFGUARDAPI is the brain behind [SurfGuard](https://github.com/notsanidhyak/SurfGuard-Chrome), a plugin for browsers which helps you surf the internet waves safely and securely. It thoroughly analyzes the site you are on and tells you whether it is safe to surf or not. The analysis is done by this custom made SurfGuard API which uses ML model having over 92.79% accuracy on training data and 92.67% accuracy on testing data.
The service is live [here](https://surfguardsays.onrender.com) and can handle upto **maximum 8** concurrent requests.
<br>
<br>

> View API's uptime [report](https://stats.uptimerobot.com/gX1q8UqzLG/794416744)

<br>


### ⚡ How to use API?
<br>

- Send a GET request to 
```
https://surfguardsays.onrender.com/getStatus?url=<url_you_wish_to_analyze>
```

- Response is sent within 10-15 seconds but may take up to 25 seconds in few scenarios (due to dependencies).
<br>

### 🤝 How to Contibute?
<br>

- Take a look at the Existing [issues](https://github.com/notsanidhyak/SurfGuardAPI/issues) or create your own issues!
- Wait for the issue to be assigned to you.
- Fork the repository.
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

If you have any feedback or suggestions please reach out to the project admin [sanidhyak](https://github.com/notsanidhyak) or you can create an [issue](https://github.com/notsanidhyak/SurfGuardAPI/issues) and mention there which new features can be added to make SURFGUARDAPI better.

