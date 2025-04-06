def parse_levels_file(file_path):
    """Parse a levels file and return a list of LevelData objects."""
    from levels import LevelData
    
    levels = []
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            
        # Split the content by level separator
        level_texts = content.split('===')
        
        for level_text in level_texts:
            if not level_text.strip():
                continue  # Skip empty sections
                
            # Parse level properties
            lines = level_text.strip().split('\n')
            
            # Check if this is a level definition
            if not lines[0].startswith('[LEVEL '):
                continue
                
            # Extract level number
            level_num = int(lines[0].replace('[LEVEL ', '').replace(']', ''))
            # Default values
            name = f"Level {level_num}"
            green_goal = 0
            red_goal = 0
            sequence = []
            grid = []
            difficulty = 1
            
            # Parse parameters and grid
            grid_started = False
            for line in lines[1:]:
                if not line.strip():
                    continue
                    
                if grid_started:
                    # Add grid row
                    grid_row = [int(cell) for cell in line.strip()]
                    grid.append(grid_row)
                elif line.startswith('grid='):
                    grid_started = True
                else:
                    # Parse key=value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key == 'name':
                            name = value
                        elif key == 'green_goal':
                            green_goal = int(value)
                        elif key == 'red_goal':
                            red_goal = int(value)
                        elif key == 'difficulty':
                            difficulty = int(value)
                        elif key == 'sequence':
                            if value:
                                sequence = value.split(',')
                        
            
            # Create level data object
            level_data = LevelData(
                level_num=level_num,
                green_goal=green_goal,
                red_goal=red_goal,
                sequence=sequence,
                grid=grid,
                name=name,
                difficulty = difficulty
            )
            
            levels.append(level_data)
            
        return levels
        
    except Exception as e:
        print(f"Error parsing levels file: {e}")
        return []

def write_levels_to_file(levels, file_path):
    """Write a list of LevelData objects to a levels file."""
    try:
        with open(file_path, 'w') as file:
            for i, level in enumerate(levels):
                # Write level header
                file.write(f"[LEVEL {level.level_num}]\n")
                file.write(f"name={level.name}\n")
                file.write(f"green_goal={level.green_goal}\n")
                file.write(f"red_goal={level.red_goal}\n")
                file.write(f"difficulty={level.difficulty}\n")
                # Write sequence
                if level.sequence:
                    file.write(f"sequence={','.join(level.sequence)}\n")
                else:
                    file.write("sequence=\n")
                
                
                # Write grid
                file.write("grid=\n")
                for row in level.grid:
                    file.write(''.join(str(cell) for cell in row) + '\n')
                
                # Add separator if not the last level
                if i < len(levels) - 1:
                    file.write("===\n")
        
        print(f"Successfully wrote levels to {file_path}")
        return True
    except Exception as e:
        print(f"Error writing levels file: {e}")
        return False


def convert_levels_to_file():
    from levels import LEVELS
    
    file_path = "levels.txt"
    return write_levels_to_file(LEVELS, file_path)