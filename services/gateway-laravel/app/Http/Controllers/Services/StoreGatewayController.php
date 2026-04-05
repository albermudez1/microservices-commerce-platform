<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Throwable;

class StoreGatewayController extends Controller
{
    public function index(): JsonResponse
    {
        $coverageServiceUrl = rtrim(env('COVERAGE_SERVICE_URL', 'http://127.0.0.1:5002'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$coverageServiceUrl}/api/stores");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de cobertura.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function show(int $id): JsonResponse
    {
        $coverageServiceUrl = rtrim(env('COVERAGE_SERVICE_URL', 'http://127.0.0.1:5002'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$coverageServiceUrl}/api/stores/{$id}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de cobertura.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function store(Request $request): JsonResponse
    {
        $coverageServiceUrl = rtrim(env('COVERAGE_SERVICE_URL', 'http://127.0.0.1:5002'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $payload = $request->only([
                'name',
                'address',
                'city',
                'latitude',
                'longitude',
                'productIds',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->post("{$coverageServiceUrl}/api/stores", $payload);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de cobertura.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function byCity(string $city): JsonResponse
    {
        $coverageServiceUrl = rtrim(env('COVERAGE_SERVICE_URL', 'http://127.0.0.1:5002'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$coverageServiceUrl}/api/stores/city/{$city}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de cobertura.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function byProduct(int $productId): JsonResponse
    {
        $coverageServiceUrl = rtrim(env('COVERAGE_SERVICE_URL', 'http://127.0.0.1:5002'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$coverageServiceUrl}/api/stores/product/{$productId}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de cobertura.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }


}
