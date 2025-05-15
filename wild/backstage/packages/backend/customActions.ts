import { createTemplateAction } from '@backstage/plugin-scaffolder-node';
import fs from 'fs-extra';
import { resolveSafeChildPath } from '@backstage/backend-common';

export const createCustomFileAction = () => {
  return createTemplateAction<{}>({
    id: 'my:custom:action',
    name: 'Create Custom File',
    description: 'Creates a custom file in the temp workspace',
    schema: {
      input: {
        type: 'object',
        properties: {},
      },
    },
    async handler(ctx) {
      const workspacePath = ctx.workspacePath;
      const filePath = resolveSafeChildPath(workspacePath, 'custom-file.txt');
      await fs.writeFile(filePath, 'This is a custom file created by my:custom:action');
      ctx.logger.info(`Created file at ${filePath}`);
    },
  });
};
