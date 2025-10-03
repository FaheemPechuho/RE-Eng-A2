"""
External Sample Code - A simple calculator with intentional code smells
"""


class Calculator:
    """A calculator with various operations."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """Add two numbers."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """Subtract b from a."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a, b):
        """Divide a by b."""
        if b == 0:  # Magic number
            return None
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    # Long Method - Calculate statistics
    def calculate_statistics(self, numbers):
        """Calculate various statistics for a list of numbers."""
        if not numbers:
            return None
        
        # Calculate sum
        total = 0
        for num in numbers:
            total += num
        
        # Calculate mean
        mean = total / len(numbers)
        
        # Calculate median
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            median = (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2
        else:
            median = sorted_numbers[n // 2]
        
        # Calculate variance
        variance_sum = 0
        for num in numbers:
            variance_sum += (num - mean) ** 2
        variance = variance_sum / len(numbers)
        
        # Calculate standard deviation
        std_dev = variance ** 0.5
        
        # Find min and max
        min_val = min(numbers)
        max_val = max(numbers)
        
        # Calculate range
        range_val = max_val - min_val
        
        return {
            'mean': mean,
            'median': median,
            'variance': variance,
            'std_dev': std_dev,
            'min': min_val,
            'max': max_val,
            'range': range_val,
            'count': len(numbers)
        }


if __name__ == '__main__':
    calc = Calculator()
    
    # Test operations
    print(calc.add(10, 5))  # Magic numbers
    print(calc.subtract(20, 8))  # Magic numbers
    print(calc.multiply(7, 6))  # Magic numbers
    print(calc.divide(100, 4))  # Magic numbers
    
    # Test statistics
    data = [23, 45, 67, 89, 12, 34, 56, 78]  # Magic numbers
    stats = calc.calculate_statistics(data)
    if stats:
        print(f"Mean: {stats['mean']:.2f}")
        print(f"Median: {stats['median']:.2f}")

