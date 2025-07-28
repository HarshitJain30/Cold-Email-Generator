import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0.3, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-70b-8192")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job,user_profile: dict):
        name = user_profile.get("name", "Your Name")
        institution = user_profile.get("institution", "Your Institution")
        batch = user_profile.get("batch", "Your Batch")
        cgpa = user_profile.get("cgpa", "Your CGPA")
        resume = user_profile.get("resume","[]")

        prompt_email = PromptTemplate.from_template(
                """
                (NO COMMENTARY)
                You are writing a professional cold email applying for the above role.
                ### INSTRUCTION:
                You are: 
                -Name: {name}
                -Institution: {institution}
                -Batch: {batch}
                -CGPA: {cgpa}
                -Resume: {resume}
                ### JOB DESCRIPTION:
                {job_description}
                Include your introduction mentioned above.

                Highlight your passion for 3 - 4 most important skills mentioned in Job Description and your eagerness to contribute meaningfully to the team.

                Also mention that you have worked on multiple projects (academic and personal) related to web development, AI, and LLM models, 
                and that you are keen to apply those skills in a professional setting.

                Include the resume link as a blue clickable hyperlink in the body(only once).

                Keep the tone professional but enthusiastic. Do not include a preamble or header.
                ### EMAIL (NO PREAMBLE)(NO HEADER):
                """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job),"name": name,"institution": institution,"batch":batch,"cgpa":cgpa,"resume":resume})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))