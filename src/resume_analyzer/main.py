#!/usr/bin/env python
from resume_analyzer.crew import ResumeAnalyzerCrew


def run():
    """
    Prompts user for inputs and runs the Resume Analyzer Crew.
    """
    print("=" * 50)
    print("MULTI-AGENT RESUME ANALYZER & JOB MATCH ADVISOR")
    print("=" * 50)
    print()
    
    resume_path = input("Enter the path to your resume file (e.g., C:/path/to/resume.txt): ").strip()
    
    if not resume_path:
        print("Error: Resume path cannot be empty!")
        return None
    
    job_url = input("Enter the job posting URL (e.g., https://company.com/jobs/123): ").strip()
    
    if not job_url:
        print("Error: Job URL cannot be empty!")
        return None
    
    print("-" * 50)
    print()
    
    print("Initializing crew...")
    print("-" * 50)
    
    crew_instance = ResumeAnalyzerCrew()
    
    inputs = {
        'resume_path': resume_path,
        'job_url': job_url
    }
    
    print("\nStarting crew execution...")
    print("This will run 3 agents sequentially:")
    print("  1. Resume Analyzer Agent → reads and analyzes resume from file")
    print("  2. Job Description Analyzer Agent → scrapes and analyzes job URL")
    print("  3. Match Advisor Agent → compares and provides recommendations")
    print("-" * 50)
    
    result = crew_instance.crew().kickoff(inputs=inputs)
    
    print("\n" + "=" * 50)
    print("FINAL MATCH ANALYSIS RESULTS")
    print("=" * 50)
    print(result)
    print("=" * 50)
    
    return result


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'resume_path': input("Enter resume path for training: "),
        'job_url': input("Enter job URL for training: ")
    }
    try:
        ResumeAnalyzerCrew().crew().train(
            n_iterations=int(input("Enter training iterations: ")),
            filename='training_output.pkl',
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Training failed: {e}")


def replay():
    """
    Replay a specific task execution from the crew.
    """
    try:
        ResumeAnalyzerCrew().crew().replay(
            task_id=input("Enter task ID to replay: ")
        )
    except Exception as e:
        raise Exception(f"Replay failed: {e}")


def test():
    """
    Test the crew execution with a single iteration.
    """
    inputs = {
        'resume_path': 'test_resume.txt',
        'job_url': 'https://example.com/test-job'
    }
    try:
        ResumeAnalyzerCrew().crew().test(
            n_iterations=1,
            openai_model_name='gpt-4o-mini',
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"Test failed: {e}")


if __name__ == "__main__":
    run()
