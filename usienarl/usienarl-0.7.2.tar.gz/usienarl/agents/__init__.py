#
# Copyright (C) 2019 Luca Pasqualini
# University of Siena - Artificial Intelligence Laboratory - SAILab
#
#
# USienaRL is licensed under a BSD 3-Clause.
#
# You should have received a copy of the license along with this
# work. If not, see <https://opensource.org/licenses/BSD-3-Clause>.

# Import scripts

from .tabular_sarsa_agent_epsilon_greedy import TabularSARSAAgentEpsilonGreedy
from .tabular_sarsa_agent_boltzmann import TabularSARSAAgentBoltzmann
from .tabular_sarsa_agent_dirichlet import TabularSARSAAgentDirichlet
from .tabular_expected_sarsa_agent_epsilon_greedy import TabularExpectedSARSAAgentEpsilonGreedy
from .tabular_expected_sarsa_agent_boltzmann import TabularExpectedSARSAAgentBoltzmann
from .tabular_expected_sarsa_agent_dirichlet import TabularExpectedSARSAAgentDirichlet
from .tabular_q_learning_agent_epsilon_greedy import TabularQLearningAgentEpsilonGreedy
from .tabular_q_learning_agent_boltzmann import TabularQLearningAgentBoltzmann
from .tabular_q_learning_agent_dirichlet import TabularQLearningAgentDirichlet

from .ddpg_agent import DDPGAgent

from .deep_sarsa_agent_epsilon_greedy import DeepSARSAAgentEpsilonGreedy
from .deep_sarsa_agent_boltzmann import DeepSARSAAgentBoltzmann
from .deep_sarsa_agent_dirichlet import DeepSARSAAgentDirichlet
from .deep_expected_sarsa_agent_epsilon_greedy import DeepExpectedSARSAAgentEpsilonGreedy
from .deep_expected_sarsa_agent_boltzmann import DeepExpectedSARSAAgentBoltzmann
from .deep_expected_sarsa_agent_dirichlet import DeepExpectedSARSAAgentDirichlet
from .deep_q_learning_agent_epsilon_greedy import DeepQLearningAgentEpsilonGreedy
from .deep_q_learning_agent_boltzmann import DeepQLearningAgentBoltzmann
from .deep_q_learning_agent_dirichlet import DeepQLearningAgentDirichlet
from .double_deep_q_learning_agent_epsilon_greedy import DoubleDeepQLearningAgentEpsilonGreedy
from .double_deep_q_learning_agent_boltzmann import DoubleDeepQLearningAgentBoltzmann
from .double_deep_q_learning_agent_dirichlet import DoubleDeepQLearningAgentDirichlet
from .dueling_deep_q_learning_agent_epsilon_greedy import DuelingDeepQLearningAgentEpsilonGreedy
from .dueling_deep_q_learning_agent_boltzmann import DuelingDeepQLearningAgentBoltzmann
from .dueling_deep_q_learning_agent_dirichlet import DuelingDeepQLearningAgentDirichlet

from .vpg_agent import VPGAgent
from .ppo_agent import PPOAgent
