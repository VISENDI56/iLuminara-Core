import pytest
from core.jepa_architecture.mpc_controller import EnergyBasedMPC

class MockWorldModel:
    def predict(self, state, action):
            return state # Dummy identity prediction
                def uncertainty(self, state):
                        return 0.1 # Low uncertainty

                        class MockCritic:
                            def compute_energy(self, embedding):
                                    return 0.5 # Constant energy

                                    def test_mpc_planning_stability():
                                        """
                                            Verifies that the MPC controller returns a valid plan
                                                and doesn't crash under nominal conditions.
                                                    """
                                                        model = MockWorldModel()
                                                            critic = MockCritic()
                                                                controller = EnergyBasedMPC(model, critic)
                                                                    
                                                                        plan = controller.plan_trajectory("START_STATE")
                                                                            assert plan is not None
                                                                                assert plan != "TRIGGER_RL_ADAPTATION"

                                                                                def test_uncertainty_trigger():
                                                                                    """
                                                                                        Verifies fallback to RL when uncertainty is high.
                                                                                            """
                                                                                                model = MockWorldModel()
                                                                                                    model.uncertainty = lambda s: 0.95 # Force high uncertainty
                                                                                                        
                                                                                                            critic = MockCritic()
                                                                                                                controller = EnergyBasedMPC(model, critic)
                                                                                                                    
                                                                                                                        plan = controller.plan_trajectory("START_STATE")
                                                                                                                            assert plan == "TRIGGER_RL_ADAPTATION"