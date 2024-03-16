### Setting Up a Static Website on Amazon S3: Step-by-Step Guide

1. **Select Your Bucket:**
   - Navigate to the Amazon S3 console.
   - Select the bucket you want to use for hosting your website.

2. **Configure Static Website Hosting:**
   - Go to `Properties` for your selected bucket.
   - Scroll down to find `Static website hosting` and click on it.

3. **Enable Static Website Hosting:**
   - In the `Static website hosting` section, toggle the switch to enable it.

4. **Set Index Document:**
   - Specify the index document for your website. Typically, this is `index.html`.

5. **Save Changes:**
   - Confirm and save the changes made to the static website hosting configuration.

6. **Manage Bucket Permissions:**
   - In the `Permissions` tab, locate `Block public access (bucket settings)`.

7. **Allow Public Access:**
   - Uncheck the option to block public access and confirm the action.

8. **Edit Bucket Policy:**
   - Navigate to the `Permissions` tab and select `Bucket Policy`.
   - Replace the existing policy with the following code:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::NAME_OF_BUCKET/*"
        }
    ]
}
```

9. **Replace Bucket Name:**
   - Replace `NAME_OF_BUCKET` in the policy with the name of your bucket.

10. **Save Policy Changes:**
    - Save the changes to update the bucket policy.

11. **Upload Website Files:**
    - If you haven't already, upload your website files to the bucket, including the `index.html` file.

12. **Access Your Website:**
    - Once the files are uploaded, go to `Properties` > `Static website hosting` to find the public URL for your website.
