import { Injectable, Logger } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { ConfigService } from '@nestjs/config';
import { firstValueFrom } from 'rxjs';

export interface MirrorPayload {
  thread_id: string;
  user_id: string;
  channel: 'web' | 'whatsapp';
  sender_type: 'user' | 'ai';
  message: string;
  timestamp: string;
}

@Injectable()
export class ControlTowerClient {
  private readonly logger = new Logger(ControlTowerClient.name);
  private readonly url: string;
  private readonly apiKey: string;
  private readonly timeout: number = 2000;

  constructor(
    private readonly httpService: HttpService,
    private readonly configService: ConfigService,
  ) {
    this.url = this.configService.get<string>('CONTROL_TOWER_URL', 'http://localhost:3000/control-tower/events');
    this.apiKey = this.configService.get<string>('CT_SECRET', 'internal-secret-key');
  }

  /**
   * Mirrors an event to the Control Tower.
   * This should be called without 'await' in the main path or via a background worker/queue.
   */
  async mirrorEvent(payload: MirrorPayload): Promise<void> {
    try {
      await firstValueFrom(
        this.httpService.post(this.url, payload, {
          headers: {
            'x-internal-api-key': this.apiKey,
            'Content-Type': 'application/json',
          },
          timeout: this.timeout,
        }),
      );
      this.logger.log(`Successfully mirrored ${payload.sender_type} message for ${payload.user_id}`);
    } catch (error) {
      // Isolate errors: log but do not throw to keep Sakhi running
      this.logger.error(
        `Failed to mirror event to Control Tower: ${error.message}`,
        error.stack,
      );
    }
  }
}
