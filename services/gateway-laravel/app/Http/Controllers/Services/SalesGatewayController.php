<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Throwable;

class SalesGatewayController extends Controller
{
    public function index(): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$salesServiceUrl}/api/sales");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function show(string $id): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$salesServiceUrl}/api/sales/{$id}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function store(Request $request): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $payload = $request->only([
                'userId',
                'productId',
                'productName',
                'quantity',
                'unitPrice',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->post("{$salesServiceUrl}/api/sales", $payload);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function byUser(int $userId): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$salesServiceUrl}/api/sales/user/{$userId}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function byDateRange(Request $request): JsonResponse
    {
        $salesServiceUrl = rtrim(env('SALES_SERVICE_URL', 'http://127.0.0.1:3000'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $queryParams = $request->only([
                'startDate',
                'endDate',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$salesServiceUrl}/api/sales/date-range/search", $queryParams);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de ventas.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }







}
