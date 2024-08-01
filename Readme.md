## Emotion Tree Talk 프로젝트 백엔드 Readme 전용 레포지토리🎄

![image](https://github.com/user-attachments/assets/00650986-3e36-402c-aa90-21bdc285bf68)

## 팀원 소개

<table>
  <tr>
    <th><strong>김민수</strong></th>
    <th><strong>이웅표</strong></th>
    <th><strong>박민아</strong></th>
    <th><strong>양의종</strong></th>
    <th><strong>최성락</strong></th>
  </tr>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/118cdd12-db99-40c4-b2f4-cf70cded4007" alt="김민수" width="150" height="150"></td>
    <td><img src="https://github.com/user-attachments/assets/7a850f92-4077-4073-987e-220d70dacc9a" alt="이웅표" width="150" height="150"></td>
    <td><img src="https://github.com/user-attachments/assets/5063b7ae-cce9-44de-a434-dda0a000964e" alt="박민아" width="150" height="150"></td>
    <td><img src="https://github.com/user-attachments/assets/0e5f674a-7eb7-4239-9d38-de28fe0f50ad" alt="양의종" width="150" height="150"></td>
    <td><img src="https://github.com/user-attachments/assets/b0c24d77-4673-4fdc-91bd-dcd302a5a466" alt="최성락" width="150" height="150"></td>
  </tr>
  <tr>
    <td><a href="https://github.com/yoyobar">@yoyobar</a></td>
    <td><a href="https://github.com/devpma">@devpma</a></td>
    <td><a href="https://github.com/ungpyolee">@ungpyolee</a></td>
    <td><a href="https://github.com/Scanf-s">@Scanf-s</a></td>
    <td><a href="https://github.com/ChoiSeongRak">@ChoiSeongRak</a></td>
  </tr>
  <tr>
    <td>Frontend 팀장</td>
    <td>Frontend</td>
    <td>Frontend</td>
    <td>Backend 팀장</td>
    <td>Backend</td>
  </tr>
</table>


## 사용 기술

### Backend
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Google Gemini 1.5 Flash](https://img.shields.io/badge/Google%20Gemini%201.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)

### Cloud Service
![AWS EC2](https://img.shields.io/badge/AWS%20EC2-FF9900?style=for-the-badge&logo=amazon-ec2&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS%20S3-569A31?style=for-the-badge&logo=amazon-s3&logoColor=white)
![AWS RDS](https://img.shields.io/badge/AWS%20RDS-527FFF?style=for-the-badge&logo=amazon-rds&logoColor=white)
![AWS CloudFront](https://img.shields.io/badge/AWS%20CloudFront-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS ELB](https://img.shields.io/badge/AWS%20ELB-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)

## Entity Relationship Diagram

![image](https://github.com/user-attachments/assets/5a5d766c-57b9-4427-8886-7192608c186c)

---

## Architecture

### 1. Cloud Architecture

![image](https://github.com/user-attachments/assets/d7152a57-4ccf-4b85-99ba-32a5436541a0)

### 2. Project Architecture

![image](https://github.com/user-attachments/assets/5adf7e75-2873-4d60-90e9-f7dd547cd7f5)

---

## Prompt Engineering

### 1. Select Google Gemini model:

	Google Gemini 1.0 pro, 1.5 flash 모델 중 현재 제공하려는 서비스와 더 알맞는 모델을 선택해야 했는데, 
	1.5 Flash 모델이 더 요청 가능한 횟수가 많으며, 응답 속도도 나쁘지 않기 때문에 1.5 Flash 모델을 선택함.
	
 	현재 제공되는 Gemini 1.5 Flash 모델은 Fine tuning 서비스가 제공되고 있지 않음. 따라서 System instruction을 최대한 자세하게 기술해야함. 
	
 	즉, Prompt engineering을 정밀하게 요구하여 원하는 답변 데이터를 얻을 수 있어야 함

### 2. 사용한 Prompt Engineering 기법

#### Few shot prompting

	가장 먼저 떠올린 것은 감정 분석 Example input, output을 제시하여 답변 제공 전 해당 Example을 통해
	따라서 풍부한 예시로 활용할 수 있는 인터넷, 일상 생활의 대화내용을 수집하여 약 30개 ~ 40개 정도 제공하였음.

#### Instruction-based(지시 기반) Prompting

	Gemini에게 특정 역할 및 작업을 수행하는 방법을 명확하게 지정함.

#### Role playing (캐릭터, 역할 지정)

	제공한 프롬프트에서, "당신은 고령의 대 마법사이며, 어쩌구 저쩌구..." 라고 지정하여 Gemini의 캐릭터를 지정하였으며,
	당신은 "심리 분석 전문가이며, 어떻게 분석해야하고, 어떻게 답변을 해야하고 어쩌구 저쩌구 ..." 라고 지정하여 
 	항상 일관적인 응답을 받을 수 있도록 지시하였음.
	
#### Explicit Constraint Setting (응답 형식 지정)

	AI가 분석한 결과를 API를 통해 Client로 전달해야 하기 때문에 Json 형식의 구조화된 데이터로만 응답을 받을 수 있도록 설정하였음

#### Contextual Understanding (대화 맥락을 이해하도록 요구)

	감정 분석 시, 한 단계씩 대화내용 감정 분석 수행 단계를 제시하였으며, 대화 한 줄, 대화 전체에 대한 내용을 이해하도록 지시하였음
	따라서 대화 한 줄 씩 이해한 내용과 대화 전체에 대한 내용을 각각 결과를 산출하여, 대화 전체 맥락을 기준으로 더 적절한 결과를 선택하도록 지시하였음

#### Error Handling and Incentive Mechanism (보상, 패널티)

	성공적으로 감정 분석을 수행하고, 고객(어플리케이션 사용자)을 만족시킨다면 $500, 엄청난 마법 도구를 제공한다는 보상을 준다고 약속하였음
	기대하는 감정 분석 내용과 다른 응답 결과를 제공하는 경우, 제공되는 보상을 차감하겠다는 패널티를 제공하였음

#### Handling Specific Linguistic Features (특정 표현에 대한 해석 지침)
	한국어로 대화시 축약어, 낱말로만 된 단어, 예시로 "ㅋㅋ", "ㄴㄴ", "ㅈㅅㅈㅅ"와 같은 낱말은 해석에 어려움을 겪을 수 있으므로 
 	다양한 예시를 추가하여 Gemini가 대화 내용 분석 시 도움을 주기 위해 지침을 제공하였음
	욕설의 경우 필터링하지 말고 대화의 강도, 억양의 강도, 감정의 정도로써 파악하라고 지시하였음

---

## 백엔드 기능 흐름

### 1. 로그인 ~ 숲 생성 과정

![image](https://github.com/user-attachments/assets/bab96f26-a640-4a3e-bb41-6fb5df58f15d)

### 2. 트리 및 채팅방 생성 과정

![image](https://github.com/user-attachments/assets/6c32e720-fb98-4673-9e52-13239d8c6017)

### 3. Dialog 송수신 과정

![image](https://github.com/user-attachments/assets/fba1454e-dbe3-47b6-a3c0-5f15dc0d3f9f)
