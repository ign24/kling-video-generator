General Information
API Domain
1
https://api-singapore.klingai.com
API Authentication
Step-1：Obtain AccessKey + SecretKey
Step-2：Every time you request the API, you need to generate an API Token according to the Fixed Encryption Method, Authorization = Bearer <API Token> in Requset Header
Encryption Method：Follow JWT（Json Web Token, RFC 7519）standard
JWT consists of three parts：Header、Payload、Signature
python
java
Copy
Collapse
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
import time
import jwt

ak = "" # fill access key
sk = "" # fill secret key

def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800, # The valid time, in this example, represents the current time+1800s(30min)
        "nbf": int(time.time()) - 5 # The time when it starts to take effect, in this example, represents the current time minus 5s
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token

authorization = encode_jwt_token(ak, sk)
print(authorization) # Printing the generated API_TOKEN
Step-3: Use the API Token generated in Step 2 to assemble the Authorization and include it in the Request Header.
Assembly format: Authorization = “Bearer XXX”, where XXX is the API Token generated in Step 2.
Note: There should be a space between Bearer and XXX.
Error Code
HTTP Status Code	Service Code	Definition of Service Code	Explaination of Service Code	Suggested Solutions
200	0	Request	-	-
401	1000	Authentication failed	Authentication failed	Check if the Authorization is correct
401	1001	Authentication failed	Authorization is empty	Fill in the correct Authorization in the Request Header
401	1002	Authentication failed	Authorization is invalid	Fill in the correct Authorization in the Request Header
401	1003	Authentication failed	Authorization is not yet valid	Check the start effective time of the token, wait for it to take effect or reissue
401	1004	Authentication failed	Authorization has expired	Check the validity period of the token and reissue it
429	1100	Account exception	Account exception	Verifying account configuration information
429	1101	Account exception	Account in arrears (postpaid scenario)	Recharge the account to ensure sufficient balance
429	1102	Account exception	Resource pack depleted or expired (prepaid scenario)	Purchase additional resource packages, or activate the post-payment service (if available)
403	1103	Account exception	Unauthorized access to requested resource, such as API/model	Verifying account permissions
400	1200	Invalid request parameters	Invalid request parameters	Check whether the request parameters are correct
400	1201	Invalid request parameters	Invalid parameters, such as incorrect key or illegal value	Refer to the specific information in the message field of the returned body and modify the request parameters
404	1202	Invalid request parameters	The requested method is invalid	Review the API documentation and use the correct request method
404	1203	Invalid request parameters	The requested resource does not exist, such as the model	Refer to the specific information in the message field of the returned body and modify the request parameters
400	1300	Trigger strategy	Trigger strategy of the platform	Check if any platform policies have been triggered
400	1301	Trigger strategy	Trigger the content security policy of the platform	Check the input content, modify it, and resend the request
429	1302	Trigger strategy	The API request is too fast, exceeding the platform’s rate limit	Reduce the request frequency, try again later, or contact customer service to increase the limit
429	1303	Trigger strategy	Concurrency or QPS exceeds the prepaid resource package limit	Reduce the request frequency, try again later, or contact customer service to increase the limit
429	1304	Trigger strategy	Trigger the platform’s IP whitelisting policy	Contact customer service
500	5000	Internal error	Server internal error	Try again later, or contact customer service
503	5001	Internal error	Server temporarily unavailable, usually due to maintenance	Try again later, or contact customer service
504	5002	Internal error	Server internal timeout, usually due to a backlog	Try again later, or contact customer service


Overview
What is Kling AI?
Kling AI, the new generation of AI creative productivity tools, is based on the image generation @Kolors and video generation @Kling technology independently developed by Kuaishou’s Large Model Algorithm Team, providing a wealth of AI images, AI videos, and related controllable editing capabilities.

For creators (individuals/enterprises), it provides an online creation platform and tools on the web and mobile devices.
For developers (individuals/enterprises), it offers API solutions.
Get access to 「Kling AI」
[1] For Users (Individuals/ Enterprises)

Web: Kling AI｜Next-generation AI Creative Studio
App：Coming soon…
[2] For Developers (Individuals/ Enterprises)

App：Coming soon…
User Guide
[1] Prompt Guide：Kling AI Best Practices

Feature List
Main Feature	Sub Feature	Sub Feature Sub-sub Feature	Feature Details
Image Generation	Text to image
Image to image	Create Task	
Supports text prompts (including positive and negative)
Supports uploading reference images and customizing the reference strength
Supports setting the aspect ratio of the generated images (width: height)
Supports generating multiple images in a single request
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Video Generation	Text to video	Create Task	
Supports text prompts (including positive and negative)
Supports customizing the reference&creativity strength
Supports different generation modes
Standard Mode：the basic mode, which is cost-effective
Professional Mode：with high performance, better generation quality
Supports camera control
Basic camera movement：6 options -Master shot：4 options
Supports setting the aspect ratio of the generated videos (width: height)
Supports setting the generated video length
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Image to video	Create Task	
Supports text prompts (including positive and negative)
Supports uploading reference images
Supports uploading Start/End Frames
Supports customizing the reference&creativity strength
Supports different generation modes
Standard Mode：with high efficiency, faster generation speed
Professional Mode：with high performance, better generation quality
Supports setting the generated video length
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Multi-Image to video	Create Task	
Supports text prompts (including positive and negative)
Supports uploading reference images（multiple）
Supports customizing the reference&creativity strength
Supports different generation modes
Standard Mode：with high efficiency, faster generation speed
Professional Mode：with high performance, better generation quality
Supports setting the generated video length
Supports setting the aspect ratio of the generated images (width: height)
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Video Extension	Create Task	
Supports uploading generated video task IDs
Supports text prompts (positive prompt only)
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Lip-Sync	Create Task	
Video ID
Video Generation Mode
Text-to-Video
Text content for generating the lip-sync video
Voice ID
Voice language
Speech speed
Audio-to-Video
Audio file
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Video Effects	Create Task	
Supports the designation of video effect scenes and allows for the input of different parameters according to the various scenes
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Text to Audio	Create Task	
Supports text prompts
Supports setting the generated audio length
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Video to Audio	Create Task	
Supports specifying Kling AI generated video IDs
Supports specifying links for uploaded videos
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes
Virtual Try-on	Kolors Virtual Try-on	Create Task	
Supports uploading reference image of model
Supports uploading reference image of clothing
Query Task (Single)	
Supports querying task status and results by single task ID
Query Task (List)	
Supports querying the status and results of all tasks
Supports querying with pagination
Callback	
Supports specifying a callback URL when creating a task
Supports proactive callback when the task status changes

Quick Access Guide
Below is a detailed guide for using the new system’s API services. We recommend following the steps for a smooth and efficient integration. If you have any questions, please feel free to contact our technical support team at any time.

Step 1: Access the KlingAI API Platform
Visit https://klingai.com/global/dev
Browse the relevant product pages
Video Generation Model： https://klingai.com/global/dev/model/video
Image Generation Model： https://klingai.com/global/dev/model/image
Intelligent Scenarios： https://klingai.com/global/dev/model/tryon


KlingAI API Platform	Video Generation Model	Image Generation Model	Intelligent Scenarios




Step 2: Resource Packages Purchasing
The three API resource packages: Video generation packages, Image generation packages, and Virtual try-on packages are fully available. You can choose packages based on your needs. Additionally, we also offer a “Trial Resource Package” for joint debugging and testing. For more details, please visit the ordering page.

Video Generation API Purchase Portal：https://klingai.com/global/dev/model/video
Image Generation API Purchase Portal：https://klingai.com/global/dev/model/image
Virtual Try-On API Purchase Portal：https://klingai.com/global/dev/model/tryon


Video Generation API Resource Package	Image Generation API Resource Package	Virtual Try-on API Resource Package



Step 3: Log in to the Developer Console
Visit https://app.klingai.com/global/dev/api-key
the Developer Console

Log in using your email. Your console account is the same as your Kling AI web account.
Step 4: Perform API Authentication
Obtain Access Key and Secret Key
Create and name your API key for easy management. You can copy the Access Key and Secret Key with one click.

Create API Key Name	One-click copy of Access Key and Secret Key	Supports enabling/disabling, renaming, and deletion



Important Notes:

Copy and save your Secret Key immediately, as it cannot be viewed again after closing the page.
It’s recommended to label the key’s purpose in the “API Key Name” for better future management. You can create up to 10 keys.


Perform JWT Verification
Follow the JWT (JSON Web Token, RFC 7519) standard. Use the specified encryption method to generate an API Token, then verify the token via JWT. Refer to the documentation at: 「Kling AI」NEW API Specification

Click JWT Verification	Paste your API Token into the text box and click Verify	If it shows [Verification successful], the API is ready for use





Construct Authorization
Use the API Token generated in Step 2 to construct the Authorization and put it in the Request Header. Format it as follows: Authorization = “Bearer XXX”. Replace XXX with the API Token from Step 2. (There must be a space between “Bearer” and XXX.)

Step 5: Call the API Service
💡
API Domain: https://api-singapore.klingai.com

Step 6: View Information in the Console



Prompting:Quick Access Guide
Below is a detailed guide for using the new system’s API services. We recommend following the steps for a smooth and efficient integration. If you have any questions, please feel free to contact our technical support team at any time.

Step 1: Access the KlingAI API Platform
Visit https://klingai.com/global/dev
Browse the relevant product pages
Video Generation Model： https://klingai.com/global/dev/model/video
Image Generation Model： https://klingai.com/global/dev/model/image
Intelligent Scenarios： https://klingai.com/global/dev/model/tryon


KlingAI API Platform	Video Generation Model	Image Generation Model	Intelligent Scenarios




Step 2: Resource Packages Purchasing
The three API resource packages: Video generation packages, Image generation packages, and Virtual try-on packages are fully available. You can choose packages based on your needs. Additionally, we also offer a “Trial Resource Package” for joint debugging and testing. For more details, please visit the ordering page.

Video Generation API Purchase Portal：https://klingai.com/global/dev/model/video
Image Generation API Purchase Portal：https://klingai.com/global/dev/model/image
Virtual Try-On API Purchase Portal：https://klingai.com/global/dev/model/tryon


Video Generation API Resource Package	Image Generation API Resource Package	Virtual Try-on API Resource Package



Step 3: Log in to the Developer Console
Visit https://app.klingai.com/global/dev/api-key
the Developer Console

Log in using your email. Your console account is the same as your Kling AI web account.
Step 4: Perform API Authentication
Obtain Access Key and Secret Key
Create and name your API key for easy management. You can copy the Access Key and Secret Key with one click.

Create API Key Name	One-click copy of Access Key and Secret Key	Supports enabling/disabling, renaming, and deletion



Important Notes:

Copy and save your Secret Key immediately, as it cannot be viewed again after closing the page.
It’s recommended to label the key’s purpose in the “API Key Name” for better future management. You can create up to 10 keys.


Perform JWT Verification
Follow the JWT (JSON Web Token, RFC 7519) standard. Use the specified encryption method to generate an API Token, then verify the token via JWT. Refer to the documentation at: 「Kling AI」NEW API Specification

Click JWT Verification	Paste your API Token into the text box and click Verify	If it shows [Verification successful], the API is ready for use





Construct Authorization
Use the API Token generated in Step 2 to construct the Authorization and put it in the Request Header. Format it as follows: Authorization = “Bearer XXX”. Replace XXX with the API Token from Step 2. (There must be a space between “Bearer” and XXX.)

Step 5: Call the API Service
💡
API Domain: https://api-singapore.klingai.com

Step 6: View Information in the Console