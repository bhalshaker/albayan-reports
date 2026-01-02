async function errorResponse(error) {
  const errorMessage = error.details.map((detail) => detail.message).join(",");
  return response.status(500).json({
    success: false,
    message: `Technical unexpected error: ${errorMessage}`,
    details: error.details,
    data: null,
  });
}

export default errorResponse;
