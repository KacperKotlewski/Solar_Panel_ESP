class Motor:
        
    def step(self, step) -> bool:
        """
        step determines the step size of the motor and the direction

        Args:
            step (int): int how many steps should make, value on minus will make step backwards and voalue on plus will make step forward

        Returns:
            bool: returns True if step was successful and False if not
        """
        return False
    
    def stop(self) -> None:
        pass