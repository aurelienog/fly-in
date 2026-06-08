from ..solver.models import SpaceTimeState

from .state import (
    HubState,
    ConnectionState,
    State,
)


class TimelineExpander:
    """Expands a sparse space-time path into a full per-timestep timeline.

    This class converts a sequence of discrete space-time states produced
    by a planner into a dense timeline suitable for simulation or rendering.

    It fills in intermediate timesteps by interpolating between:
        - waiting periods (remaining in the same hub)
        - movement along connections (progress-based states)

    The resulting timeline contains both HubState and ConnectionState
    objects for each timestep.
    """

    def expand(
        self,
        path: list[SpaceTimeState]
    ) -> list[State]:
        """Expand a compressed space-time path into a full timeline.

        The input path typically contains only key transitions between
        hubs at discrete timesteps. This method reconstructs all
        intermediate states to make the trajectory continuous in time.

        Args:
            path: Ordered list of space-time states produced by a planner.

        Returns:
            A list of expanded states covering every timestep between the
            first and last state in the path. Returns an empty list if
            the input path is empty.
        """

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
                progress = (
                    t - previous.timestep
                ) / (
                    current.timestep - previous.timestep
                )
                timeline.append(ConnectionState(
                    connection=connection,
                    timestep=t,
                    from_hub=previous.hub,
                    to_hub=current.hub,
                    progress=progress)
                    )

            timeline.append(
                HubState(
                    hub=current.hub,
                    timestep=current.timestep
                )
            )

        return timeline
