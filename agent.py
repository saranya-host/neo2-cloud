from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.agents.llms import google
from livekit.agents.audio import noise_cancellation
from prompt import AGENT_INSTRUCTIONS, AGENT_RESPONSE

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTIONS)

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",
            voice="Fenrir",  # You can change to Onyx, Wave, Ember, etc.
            temperature=0.8,
            instructions=AGENT_INSTRUCTIONS,
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    async for event in session.listen():
        if event.is_user_message:
            await session.generate_reply(
                text=event.text,
                instructions=AGENT_INSTRUCTIONS + "\n" + AGENT_RESPONSE
            )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
