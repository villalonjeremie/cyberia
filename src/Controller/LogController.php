<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\Logs;

final class LogController
{
    #[Route('/api/log',name: 'api_log', methods: ['POST'])]
    public function __invoke(Request $request, EntityManagerInterface $em): JsonResponse
    {
        $data = $request->getContent();

        if (empty($data)) {
            return new JsonResponse(
                [
                    'status' => 'error',
                    'message' => 'Empty request body'
                ],
                JsonResponse::HTTP_BAD_REQUEST
            );
        }

        $lines = explode("\n", trim($data));
        $validLines = [];

        foreach ($lines as $line) {
            if (!$this->isValidApacheLogLine($line)) {
                return new JsonResponse(
                    [
                        'status' => 'error',
                        'message' => 'Wrong log format',
                        'line' => trim($line)
                    ],
                    JsonResponse::HTTP_UNPROCESSABLE_ENTITY 
                );
            }
        }

        $logDir = __DIR__ . '/../../python';

        if (!is_dir($logDir)) {
            mkdir($logDir, 0755, true);
        }

        $logFile = $logDir . '/access.log';
        file_put_contents($logFile, $data, FILE_APPEND);

        return new JsonResponse([
            'status' => 'ok',
            'received' => $data,
        ]);
    }

    private function isValidApacheLogLine(string $line): bool
    {
        $pattern = '/^(\d{1,3}(?:\.\d{1,3}){3})\s-\s-\s\[\d{2}\/[A-Za-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2}\s[+-]\d{4}\]\s"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s\/[^"]*\sHTTP\/\d\.\d"\s\d+\s\d+$/';
        return preg_match($pattern, trim($line)) === 1;
    }

            /** 
        if (!is_array($data)) {
            return new JsonResponse(
                ['error' => 'Invalid JSON'],
                400
            );
        }

        $logs = new Logs();
        $logs->setSecurityType($data['type']);
        $logs->setLogsJson($data['content']);
        $logs->setCreatedAt($logs->getCreatedAt());
        $logs->setIsProcessed(false);

        $em->persist($logs);
        $em->flush();

        return new JsonResponse([
            'status' => 'ok',
            'received' => $data,
        ]);**/
}
