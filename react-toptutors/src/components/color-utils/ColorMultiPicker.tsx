// @mui
import { Box, Checkbox, Typography } from '@mui/material';
//
import Icon from './Icon';
import { ColorMultiPickerProps } from './types';

// ----------------------------------------------------------------------

export default function ColorMultiPicker({
  colors,
  colorOptionsText,
  selected,
  onChangeColor,
  sx,
  ...other
}: ColorMultiPickerProps) {
  return (
    <Box sx={sx}>
      {colors.map((color, index) => {
        const whiteColor = color === '#FFFFFF' || color === 'white';

        return (
          <>
            {' '}
            <Typography
              variant="caption"
              sx={{
                p: 2,
                color: 'text.secondary',
                fontWeight: 'fontWeightMedium',
              }}
            >
              {colorOptionsText[index]}
            </Typography>
            <Checkbox
              key={color}
              size="small"
              value={color}
              color="default"
              checked={selected.includes(color)}
              onChange={() => onChangeColor(color)}
              icon={<Icon whiteColor={whiteColor} />}
              checkedIcon={<Icon checked whiteColor={whiteColor} />}
              sx={{
                color,
                '&:hover': { opacity: 0.72 },
                '& svg': { width: 12, height: 12 },
              }}
              {...other}
            />
          </>
        );
      })}
    </Box>
  );
}
