#!/usr/bin/env python
# Copyright (C) 2011 Alejandro Varas
# based on code taken from http://www.bonf.net/2007/05/18/so/
######################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

"""pygame-based stopwatch."""

from __future__ import division

import datetime

import pygame
import pygame.font
from pygame.colordict import THECOLORS


def create_window():
    """Return draw function, which takes a text parameter."""
    pygame.init()

    pygame.display.set_caption('stopwatch')
    resolution = pygame.display.list_modes()[0]
    surface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)

    # Get highest font size that fits resolution width.
    font_size = int(resolution[1] / 1.2)
    font_size_fits = False
    max_string_length = resolution[0] // 8 * 7

    while not font_size_fits:
        font = pygame.font.SysFont('courier new', font_size)
        font_rect = font.size("00:00:00,00")
        if font_rect[0] > max_string_length:
            font_size = font_size - 10
        else:
            font_size_fits = True

    # Get the point to draw the font in the midle of the screen.
    font_blit_point = (resolution[0] // 16,
                       resolution[1] // 2 - font_rect[1] // 2)

    def draw(text):
        """Draw text."""
        # Fill the screen with white, to erase the previous time.
        surface.fill(THECOLORS["white"])
        surface.blit(font.render(text, 1, THECOLORS["black"]),
                     font_blit_point)

        pygame.display.flip()

    return draw


def milliseconds_to_text(milliseconds):
    """Return text representation."""
    current_time = datetime.time(
        (milliseconds // 1000) // 3600,
        (milliseconds // 1000) // 60 % 60,
        (milliseconds // 1000) % 60)

    hundredth_of_millisecond = str(milliseconds)[-3:][:2]
    return ','.join((current_time.strftime("%H:%M:%S"),
                    hundredth_of_millisecond))


def main():
    """Entry point."""
    draw = create_window()

    fullscreen = True
    running = False
    milliseconds = 0
    start_tick = 0  # The number of ticks when we began counting.

    while True:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            break

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                break

            if event.key == pygame.K_SPACE:
                if not running:
                    # Starting the timer, so set the tick count reference to
                    # the current tick count plus the last tick count.
                    start_tick = pygame.time.get_ticks() - milliseconds

                running = not running

            elif event.key == pygame.K_r:
                milliseconds = 0
                running = False

            elif event.key == pygame.K_f:
                fullscreen = not fullscreen
                video_flags = (
                    fullscreen and pygame.FULLSCREEN) | (
                        not fullscreen and pygame.RESIZABLE)
                pygame.display.set_mode((0, 0), video_flags)

        if running:
            milliseconds = (pygame.time.get_ticks() - start_tick)

        draw(milliseconds_to_text(milliseconds))

        pygame.time.wait(1)


if __name__ == '__main__':
    main()
