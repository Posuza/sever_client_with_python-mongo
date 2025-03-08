### Available Commands

The client supports the following commands:

- `gad` - Get all user data
- `login` - User login
- `reg` - Register a new user (voter or candidate)
- `vote` - Vote for a candidate
- `candidate_info` - Get information about all candidates
- `emailcheck` - Check if an email exists in the system
- `transfer_email` - Check if a transfer email exists
- `update_point` - Update points after a transfer

## Database Structure

The application uses two main collections in MongoDB:

1. **user_info**: Stores voter information
   - email
   - password
   - name
   - phone
   - info
   - point

2. **candidate**: Stores candidate information
   - name
   - email
   - password
   - phone
   - info
   - vote_point

## Project Structure

- `tcp_server_mongo.py` - Server-side implementation
- `tcp_client_mongo.py` - Client-side implementation

## Security Considerations

This is a demonstration project and has several security limitations:
- Passwords are stored in plain text
- No encryption for data transmission
- Limited input validation

For production use, implement proper security measures like password hashing, SSL/TLS encryption, and comprehensive input validation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
