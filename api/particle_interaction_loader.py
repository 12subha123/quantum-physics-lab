from api.main import app
from api.particle_interaction import router

if router not in app.router.routes:
    app.include_router(router)

print("Particle interaction router loaded.")
