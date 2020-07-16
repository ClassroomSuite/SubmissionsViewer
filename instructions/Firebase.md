# Firebase
* You can keep the same Firebase project for across semesters
* You should empty your database at least after each semester to reduce download size  
* Generous free plan  
[](https://firebase.google.com/)
1. Create a project ([Follow instructions](https://console.firebase.google.com/))
2. Add a Realtime Database
    * https://firebase.google.com/products/realtime-database/
    * https://firebase.google.com/docs/database
3. Read about [pricing](https://firebase.google.com/pricing)
and [FAQ](https://firebase.google.com/support/faq#pricing)
4. Change Realtime Database [Rules](https://firebase.google.com/docs/database/security/quickstart#public) to the following
    * This will allow public access to the database
    ```
    {
      "rules": {
        ".read": true,
        ".write": true
      }
    }
    ```
5. Find your Realtime Database link
    * It will have the following format: https://%yourproject%.firebaseio.com/
    * e.g.: https://inf1007.firebaseio.com/
6. Append the following to your link: .json?
    * e.g.: https://inf1007.firebaseio.com/.json?
7. Test your link in a web browser
    * You should see the contents of your database
8. Save your link, you'll need it later