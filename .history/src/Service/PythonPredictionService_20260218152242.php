<?php

namespace App\Service;

use Symfony\Contracts\HttpClient\HttpClientInterface;

class PythonPredictionService
{
    private HttpClientInterface $client;
    private string $pythonApiUrl;
    private string $pythonApiKey;

    public function __construct(
        HttpClientInterface $client,
        string $pythonApiUrl,
        string $pythonApiKey
    ) {
        $this->client = $client;
        $this->pythonApiUrl = $pythonApiUrl;
        $this->pythonApiKey = $pythonApiKey;
    }

    public function sendLogFile(string $filePath): array
    {
        try {
            if (!file_exists($filePath)) {
                throw new \Exception("Fichier introuvable : $filePath");
            }

            $fileContents = file_get_contents($filePath);
            $jsonData = [
                'filename' => basename($filePath),
                'content_base64' => base64_encode($fileContents)
            ];

            $response = $this->client->request(
                'POST',
                $this->pythonApiUrl . '/predict',
                [
                    'headers' => [
                    'X-API-KEY' => $this->pythonApiKey,
                    'Content-Type' => 'application/json'
                    ],
                    'json' => $jsonData,
                    'timeout' => 60,
                ]
            );

            return $response->toArray();

        } catch (\Throwable $e) {

            return [
                'status' => 'error',
                'message' => $e->getMessage(),
            ];
        }
    }

}
