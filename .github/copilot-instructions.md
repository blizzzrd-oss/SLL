---
applyTo: "**"
---
# Project general coding standards

## Clean Code
- never use global variables
- never use local imports
- avoid circular imports by refactoring
- don't use hard coded values, use variables in matching config files
- make it modular if possible

## Naming Conventions
- Use PascalCase for component names, interfaces, and type aliases
- Use camelCase for variables, functions, and methods
- Prefix private class members with underscore (_)
- Use ALL_CAPS for constants

## Error Handling
- Use try/catch blocks for async operations
- Implement proper error boundaries in React components
- Always log errors with contextual information