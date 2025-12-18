from resume_analyzer.tools.resume_parser import parse_resume_file
from resume_analyzer.tools.job_scraper import scrape_job_url
from crewai.project import CrewBase, agent, crew, task
from crewai import Agent, Crew, Process, Task


@CrewBase
class ResumeAnalyzerCrew:
    """
    Multi-Agent Resume Analyzer Crew.
    Coordinates agents to analyze a candidate's resume against a job description.
    """
    
    @agent
    def resume_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_analyzer'],
            tools=[parse_resume_file],
            verbose=True
        )
    
    @agent
    def job_description_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['job_description_analyzer'],
            tools=[scrape_job_url],
            verbose=True
        )
    
    @agent
    def match_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['match_advisor'],
            verbose=True
        )
    
    @task
    def analyze_resume_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_resume_task']
        )
    
    @task
    def analyze_job_description_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_job_description_task']
        )
    
    @task
    def generate_match_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_match_analysis_task']
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Creates the Resume Analyzer Crew with sequential process.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
