// Utility function to handle error responses
async function errorResponse(error, response) {
  // Extract error details
  const details =
    error && error.details
      ? error.details
      : [{ message: error?.message || "Unexpected error" }];
  // Construct error message
  const errorMessage = details.map((detail) => detail.message).join(", ");
  // Send error response
  return response.status(error?.statusCode || 500).json({
    success: false,
    message: `Technical unexpected error: ${errorMessage}`,
    details,
    data: null,
  });
}

export default errorResponse;
