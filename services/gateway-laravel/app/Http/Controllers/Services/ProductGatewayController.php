<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Throwable;

class ProductGatewayController extends Controller
{
    public function index(): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$catalogServiceUrl}/api/products");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de catálogo e inventario.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function show(int $id): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$catalogServiceUrl}/api/products/{$id}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de catálogo e inventario.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function stock(int $id): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->get("{$catalogServiceUrl}/api/products/{$id}/stock");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de catálogo e inventario.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }    

    public function store(Request $request): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $payload = $request->only([
                'name',
                'description',
                'price',
                'stock',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->post("{$catalogServiceUrl}/api/products", $payload);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de catálogo e inventario.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function update(Request $request, int $id): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $payload = $request->only([
                'name',
                'description',
                'price',
                'stock',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->put("{$catalogServiceUrl}/api/products/{$id}", $payload);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de catálogo e inventario.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function destroy(int $id): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->delete("{$catalogServiceUrl}/api/products/{$id}");

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de catálogo e inventario.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function decreaseStock(Request $request, int $id): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $payload = $request->only([
                'quantity',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->patch("{$catalogServiceUrl}/api/products/{$id}/stock/decrease", $payload);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de catálogo e inventario.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }

    public function increaseStock(Request $request, int $id): JsonResponse
    {
        $catalogServiceUrl = rtrim(env('CATALOG_INVENTORY_SERVICE_URL', 'http://127.0.0.1:5001'), '/');
        $gatewayServiceToken = env('GATEWAY_SERVICE_TOKEN');

        try {
            $payload = $request->only([
                'quantity',
            ]);

            $response = Http::withHeaders([
                'X-Gateway-Token' => $gatewayServiceToken,
                'Accept' => 'application/json',
            ])->timeout(10)->patch("{$catalogServiceUrl}/api/products/{$id}/stock/increase", $payload);

            return response()->json($response->json(), $response->status());
        } catch (Throwable $exception) {
            return response()->json([
                'message' => 'No fue posible comunicarse con el microservicio de catálogo e inventario.',
                'error' => $exception->getMessage(),
            ], 503);
        }
    }






}
