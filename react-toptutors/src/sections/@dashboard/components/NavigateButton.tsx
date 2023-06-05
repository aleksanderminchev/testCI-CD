/* follow this path to get to where the code is inspired from in the Minimal_TypeScript_v4.2.0:

src/sections/@dashboard/file/FilePanel
*/
import { Link as RouterLink } from 'react-router-dom';
// @mui
import { Box, Button, StackProps } from '@mui/material';
// components

import Iconify from '../../../components/iconify';

// ----------------------------------------------------------------------

interface Props extends StackProps {
  link?: string;
  onOpen?: VoidFunction;
}

export default function NavigateButton({ link, onOpen, sx, ...other }: Props) {
  return (
    <Box sx={{ p: 2, textAlign: 'right' }}>
      {link && (
        <Button
          to={link}
          component={RouterLink}
          size="small"
          color="inherit"
          endIcon={<Iconify icon="eva:chevron-right-fill" />}
        >
          View All
        </Button>
      )}
    </Box>
  );
}
