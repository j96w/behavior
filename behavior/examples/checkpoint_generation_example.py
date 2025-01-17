"""Save checkpoints from a BEHAVIOR demo."""
import logging
import os

import igibson
from igibson.examples.learning.demo_replaying_example import replay_demo_with_determinism_check
from igibson.utils.checkpoint_utils import save_checkpoint

import behavior


def create_checkpoints(demo_file, checkpoint_directory, checkpoint_every_n_steps):
    # Create a step callback function to feed replay steps into checkpoints.
    def step_callback(env, _):
        if not env.task.current_success and env.simulator.frame_count % checkpoint_every_n_steps == 0:
            save_checkpoint(env.simulator, checkpoint_directory)

    print("Replaying demo and saving checkpoints")
    replay_demo_with_determinism_check(demo_file, mode="headless", step_callbacks=[step_callback])


def main(selection="user", headless=False, short_exec=False):
    """
    Opens a demo and creates checkpoints every N steps
    Checkpoints can be used to initialize the simulation at those states, for example, for RL
    """
    print("*" * 80 + "\nDescription:" + main.__doc__ + "\n" + "*" * 80)

    demo_file = os.path.join(
        igibson.ig_dataset_path,
        "tests",
        "cleaning_windows_0_Rs_int_2021-05-23_23-11-46.hdf5",
    )
    checkpoint_directory = os.path.join(
        behavior.examples_path,
        "data",
        "checkpoints",
    )
    os.makedirs(checkpoint_directory, exist_ok=True)

    steps_between_checkpoints = 30 if not short_exec else 300
    create_checkpoints(demo_file, checkpoint_directory, steps_between_checkpoints)


RUN_AS_TEST = False  # Change to True to run this example in test mode
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if RUN_AS_TEST:
        main(selection="random", headless=True, short_exec=True)
    else:
        main()
