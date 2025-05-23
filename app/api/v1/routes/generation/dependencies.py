from app.services.generation import GenerationService


def get_generation_service() -> GenerationService:
    return GenerationService() 