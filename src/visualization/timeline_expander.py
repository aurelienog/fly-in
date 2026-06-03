from ..solver.models import SpaceTimeState

from .state import (
    HubState,
    ConnectionState,
    State,
)


class TimelineExpander:

    def expand(
        self,
        path: list[SpaceTimeState]
    ) -> list[State]:

        if not path:
            return []

        timeline: list[State] = [
            HubState(
                hub=path[0].hub,
                timestep=path[0].timestep
            )
        ]

        for previous, current in zip(
            path,
            path[1:]
        ):

            # dt = (
            #     current.timestep
            #     -
            #     previous.timestep
            # )

            #
            # WAIT
            #

            if previous.hub == current.hub:

                for t in range(
                    previous.timestep + 1,
                    current.timestep + 1
                ):
                    timeline.append(
                        HubState(
                            hub=current.hub,
                            timestep=t
                        )
                    )

                continue

            #
            # MOVE
            #

            connection = (
                previous.hub
                .get_connection(current.hub)
            )

            for t in range(
                previous.timestep + 1,
                current.timestep
            ):
                timeline.append(ConnectionState(
                    connection=connection,
                    timestep=t,
                    from_hub=previous.hub,
                    to_hub=current.hub)
                    )

            timeline.append(
                HubState(
                    hub=current.hub,
                    timestep=current.timestep
                )
            )

        return timeline
