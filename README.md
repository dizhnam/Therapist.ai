# TreeHacks2024

# Therapist.ai

## Introduction

Welcome to Therapist.ai, a revolutionary platform designed to transform the counseling and therapy landscape. Our goal is to enhance the efficiency and effectiveness of counseling sessions by providing counselors and therapists with powerful AI-driven tools. With Therapist.ai, professionals can streamline their workflows, gain valuable insights from patient interactions, and ultimately deliver personalized care to their clients.

## Inspiration

Therapist.ai was born out of a profound desire to address the challenges faced by counselors and therapists in managing extensive patient case files while striving to deliver personalized care. We envisioned a solution that seamlessly integrates into practitioners' workflows, empowering them to provide unparalleled support and care to their clients, regardless of session volume or complexity.

## What it Does

Therapist.ai serves as an invaluable AI assistant powered by LangChain. It streamlines counselors' and therapists' workflows by efficiently summarizing patient case files and providing tailored recommendations derived from past and ongoing interactions. By retaining past context, Therapist.ai enables professionals to better support their clients on their journey towards healing and growth.

## How We Built It

Therapist.ai is comprised of three main components:

1. **Agents powered by Intel's "Prediction Guard" LLM models:** These agents store user data into a vector database and contextualize the data. They support the core logic of our application, including summarizing user details based on PDF case data and providing tailored suggestions to counselors.
  
2. **Frontend:** Built in ReactJS, the frontend utilizes APIs exposed by the backend to showcase the power of our AI companion. Canva.dev was used for some components.
  
3. **API Backend:** Built with Flask, the backend bridges the gap between the Agent and the Frontend. Deployment is done using Vercel, as demonstrated in the demo.

We utilized a combination of programming languages and technologies, including Python for backend development, React for the frontend, and various APIs for data analysis and natural language processing. Cloud services were used for hosting and deployment.

## Challenges We Ran Into

One major challenge was the lack of expertise in frontend development, which required us to learn and deploy simultaneously. Canva.dev proved to be immensely helpful in overcoming this challenge. Additionally, integrating LanceDB, a relatively new database technology, presented challenges due to limited community support. We also faced difficulties with LLM chaining to provide context with chat history and user details.

## Accomplishments We're Proud Of

We're proud to have developed a functional end-to-end prototype of Therapist.ai within the timeframe of the hackathon. Our platform demonstrates the potential to significantly improve the workflow of counselors and therapists, benefiting both professionals and their clients. We believe Therapist.ai could be a game-changer for counselors helping patients fight mental health issues.

## What We Learned

Building Therapist.ai provided us with valuable experience in full-stack web development, RAG, VectorDB, LangChain, and various other technologies that were previously unfamiliar to us. We also discovered amazing companies providing solutions that we integrated into our application, including Intel's Prediction Guard, Canva.dev components, and deployment via Vercel.

## What's Next for Therapist.ai

Moving forward, we envision a comprehensive evolution of Therapist.ai aimed at empowering users on their mental wellness journey. We're committed to refining and enhancing the platform to offer a personalized space where individuals can seamlessly upload their daily thoughts. Leveraging advanced algorithms and user data, Therapist.ai will intelligently suggest affirmations and curated meditation resources tailored to each user's unique needs and emotional state.

Furthermore, we're exploring innovative solutions such as blockchain technology to securely store patient case files. This ensures seamless transitions between therapists or counselors without any loss of crucial information. By implementing blockchain, we guarantee the integrity and accessibility of patient records, fostering continuity of care and empowering individuals to receive the support they need, wherever they may be.

## Demo

To see Therapist.ai in action, check out our demo [here](https://youtu.be/1KA1iihK3-4?si=R3pFc6LXDz4OApKn).

## Contributors

* Manikanta Sanjay Veera
* Ashish Agarwal
* Mridang Kejriwal
* Mohammed Danish Hussain

